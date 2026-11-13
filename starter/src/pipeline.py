import os
import re
import json
import time
import pypdf
import chromadb
from sentence_transformers import SentenceTransformer

os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['TRANSFORMERS_OFFLINE'] = '1'

print("Initializing SentenceTransformer ('all-MiniLM-L6-v2', local offline)...")
EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2', local_files_only=True)

# 1. READ DOCUMENTS
def load_documents():
    with open('data/manifest.json', encoding='utf-8') as f:
        manifest = json.load(f)
    
    docs_pages = []
    for doc_meta in manifest['documents']:
        pdf_path = doc_meta['source_path']
        source_id = doc_meta['source_id']
        year = doc_meta['year']
        start_p, end_p = doc_meta['content_pages_range']
        
        reader = pypdf.PdfReader(pdf_path)
        for page_num in range(start_p, end_p + 1):
            text = reader.pages[page_num - 1].extract_text() or ''
            # Normalize whitespace
            norm_text = ' '.join(text.split())
            docs_pages.append({
                'document_id': source_id,
                'source': doc_meta['title'],
                'year': year,
                'page': page_num,
                'text': norm_text
            })
    return docs_pages

# 2. CHUNKING STRATEGY A: Fixed-size (500 chars, overlap 50)
def chunk_strategy_a(docs_pages, chunk_size=500, overlap=50):
    chunks = []
    chunk_id_seq = 1
    for page_info in docs_pages:
        text = page_info['text']
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]
            if len(chunk_text.strip()) > 30:
                chunks.append({
                    'chunk_id': f"A_{page_info['document_id']}_p{page_info['page']}_{chunk_id_seq}",
                    'document_id': page_info['document_id'],
                    'source': page_info['source'],
                    'year': page_info['year'],
                    'page': page_info['page'],
                    'section': 'General',
                    'strategy': 'A_Fixed',
                    'text': chunk_text
                })
                chunk_id_seq += 1
            start += (chunk_size - overlap)
            if end >= len(text):
                break
    return chunks

# 3. CHUNKING STRATEGY B: Structure/Article-based
def chunk_strategy_b(docs_pages):
    chunks = []
    chunk_id_seq = 1
    
    # We group text across pages by Article (Điều x)
    current_doc = None
    buffer_text = ""
    current_meta = {}
    
    for page_info in docs_pages:
        text = page_info['text']
        # Find articles in text
        # Pattern like: Điều 19. ...
        articles = list(re.finditer(r'(Điều\s+\d+\.[^.]+?\.)', text))
        
        if not articles:
            # Append to ongoing buffer or emit as paragraph
            chunks.append({
                'chunk_id': f"B_{page_info['document_id']}_p{page_info['page']}_{chunk_id_seq}",
                'document_id': page_info['document_id'],
                'source': page_info['source'],
                'year': page_info['year'],
                'page': page_info['page'],
                'section': 'Nội dung tiếp nối',
                'strategy': 'B_Structure',
                'text': text[:1000] # bounded chunk
            })
            chunk_id_seq += 1
            if len(text) > 1000:
                chunks.append({
                    'chunk_id': f"B_{page_info['document_id']}_p{page_info['page']}_{chunk_id_seq}",
                    'document_id': page_info['document_id'],
                    'source': page_info['source'],
                    'year': page_info['year'],
                    'page': page_info['page'],
                    'section': 'Nội dung tiếp nối (tiếp)',
                    'strategy': 'B_Structure',
                    'text': text[950:]
                })
                chunk_id_seq += 1
        else:
            # Split page by articles
            indices = [m.start() for m in articles] + [len(text)]
            # Text before first article
            if indices[0] > 0:
                lead = text[:indices[0]].strip()
                if len(lead) > 30:
                    chunks.append({
                        'chunk_id': f"B_{page_info['document_id']}_p{page_info['page']}_{chunk_id_seq}",
                        'document_id': page_info['document_id'],
                        'source': page_info['source'],
                        'year': page_info['year'],
                        'page': page_info['page'],
                        'section': 'Phần mở đầu',
                        'strategy': 'B_Structure',
                        'text': lead
                    })
                    chunk_id_seq += 1
            
            for i in range(len(articles)):
                art_name = articles[i].group(1).strip()
                art_content = text[indices[i]:indices[i+1]].strip()
                if len(art_content) > 30:
                    # If article is very long, break into logical clauses
                    if len(art_content) <= 1200:
                        chunks.append({
                            'chunk_id': f"B_{page_info['document_id']}_p{page_info['page']}_{chunk_id_seq}",
                            'document_id': page_info['document_id'],
                            'source': page_info['source'],
                            'year': page_info['year'],
                            'page': page_info['page'],
                            'section': art_name,
                            'strategy': 'B_Structure',
                            'text': art_content
                        })
                        chunk_id_seq += 1
                    else:
                        part1 = art_content[:1000]
                        part2 = art_name + " (tiếp): " + art_content[950:]
                        chunks.append({
                            'chunk_id': f"B_{page_info['document_id']}_p{page_info['page']}_{chunk_id_seq}",
                            'document_id': page_info['document_id'],
                            'source': page_info['source'],
                            'year': page_info['year'],
                            'page': page_info['page'],
                            'section': art_name,
                            'strategy': 'B_Structure',
                            'text': part1
                        })
                        chunk_id_seq += 1
                        chunks.append({
                            'chunk_id': f"B_{page_info['document_id']}_p{page_info['page']}_{chunk_id_seq}",
                            'document_id': page_info['document_id'],
                            'source': page_info['source'],
                            'year': page_info['year'],
                            'page': page_info['page'],
                            'section': art_name + " (tiếp)",
                            'strategy': 'B_Structure',
                            'text': part2
                        })
                        chunk_id_seq += 1
    return chunks

# 4. INGESTION TO CHROMADB
def build_collection(collection_name, chunks, client):
    # reset if exists
    try:
        client.delete_collection(collection_name)
    except:
        pass
    
    coll = client.create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}
    )
    
    print(f"Embedding and inserting {len(chunks)} chunks into '{collection_name}'...")
    start_t = time.time()
    
    batch_size = 64
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        texts = [c['text'] for c in batch]
        ids = [c['chunk_id'] for c in batch]
        metadatas = [{
            'document_id': c['document_id'],
            'source': c['source'],
            'year': c['year'],
            'page': c['page'],
            'section': c['section'],
            'strategy': c['strategy']
        } for c in batch]
        
        embeddings = EMBEDDING_MODEL.encode(texts).tolist()
        coll.upsert(ids=ids, documents=texts, embeddings=embeddings, metadatas=metadatas)
    
    elapsed = time.time() - start_t
    print(f"Completed '{collection_name}' in {elapsed:.2f}s")
    return coll, elapsed

# 5. RETRIEVAL & BENCHMARK RUNNER
def evaluate_strategy(coll, strategy_name, benchmark_questions, use_filter=False):
    results = []
    
    for q in benchmark_questions:
        q_text = q['question']
        q_emb = EMBEDDING_MODEL.encode([q_text]).tolist()
        
        # Apply filter only for Strategy C when question has filter
        where_filter = None
        if use_filter and q['filter'] is not None:
            where_filter = {'year': q['filter']['year']}
        
        query_res = coll.query(
            query_embeddings=q_emb,
            n_results=3,
            where=where_filter
        )
        
        top3_ids = query_res['ids'][0]
        top3_docs = query_res['documents'][0]
        top3_metas = query_res['metadatas'][0]
        top3_distances = query_res['distances'][0]
        
        # Determine Hit@1 and Hit@3
        gold_source = q['gold_source_id']
        gold_page = q['gold_page']
        evidence_quote = ' '.join(q['evidence_quote'].split())
        
        hits = []
        for rank in range(len(top3_ids)):
            meta = top3_metas[rank]
            doc_text = ' '.join(top3_docs[rank].split())
            
            is_gold_doc = (meta['document_id'] == gold_source)
            is_gold_page = (meta['page'] == gold_page)
            has_evidence = (evidence_quote in doc_text)
            
            is_hit = (is_gold_doc and is_gold_page and has_evidence)
            hits.append({
                'rank': rank + 1,
                'chunk_id': top3_ids[rank],
                'document_id': meta['document_id'],
                'page': meta['page'],
                'is_hit': is_hit,
                'score': round(1.0 - top3_distances[rank], 4),
                'text_snippet': doc_text[:120]
            })
        
        hit_at_1 = hits[0]['is_hit'] if len(hits) > 0 else False
        hit_at_3 = any(h['is_hit'] for h in hits)
        
        # Filter compliance
        filter_compliant = True
        if where_filter is not None:
            for m in top3_metas:
                if m['year'] != where_filter['year']:
                    filter_compliant = False
        
        results.append({
            'question_id': q['id'],
            'split': q['split'],
            'strategy': strategy_name,
            'question': q_text,
            'gold_source': gold_source,
            'gold_page': gold_page,
            'has_filter': (q['filter'] is not None),
            'filter_used': where_filter,
            'filter_compliant': filter_compliant if (q['filter'] is not None) else None,
            'hit_at_1': hit_at_1,
            'hit_at_3': hit_at_3,
            'top3': hits
        })
        
    return results

if __name__ == '__main__':
    print("Loading documents...")
    docs_pages = load_documents()
    print(f"Loaded {len(docs_pages)} pages from manifest.")
    
    print("\n--- Generating Chunks ---")
    chunks_a = chunk_strategy_a(docs_pages)
    chunks_b = chunk_strategy_b(docs_pages)
    print(f"Strategy A (Fixed 500/50): {len(chunks_a)} chunks")
    print(f"Strategy B (Structure/Article): {len(chunks_b)} chunks")
    
    # Persistent Chroma Client
    db_path = './starter/chroma_db'
    client = chromadb.PersistentClient(path=db_path)
    
    coll_a, time_a = build_collection("strategy_a_fixed", chunks_a, client)
    coll_b, time_b = build_collection("strategy_b_structure", chunks_b, client)
    
    with open('data/benchmark_questions.json', encoding='utf-8') as f:
        bench_questions = json.load(f)
    
    print("\n--- Running Benchmark across 3 Strategies ---")
    results_a = evaluate_strategy(coll_a, "Strategy_A_Fixed", bench_questions, use_filter=False)
    results_b = evaluate_strategy(coll_b, "Strategy_B_Structure", bench_questions, use_filter=False)
    results_c = evaluate_strategy(coll_b, "Strategy_C_Filtered", bench_questions, use_filter=True)
    
    all_results = {
        'metadata': {
            'embedding_model': 'sentence-transformers/all-MiniLM-L6-v2',
            'dimensions': 384,
            'vector_store': 'ChromaDB 1.5.9',
            'metric': 'cosine',
            'chunk_counts': {'A': len(chunks_a), 'B': len(chunks_b), 'C': len(chunks_b)},
            'ingest_time_seconds': {'A': round(time_a, 2), 'B': round(time_b, 2), 'C': round(time_b, 2)},
            'cost_usd': 0.0
        },
        'results_A': results_a,
        'results_B': results_b,
        'results_C': results_c
    }
    
    os.makedirs('starter/results', exist_ok=True)
    with open('starter/results/benchmark_trace.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print("\nBenchmark results saved to 'starter/results/benchmark_trace.json'!")
