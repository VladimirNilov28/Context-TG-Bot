from app.services.embeddings import get_embedding
from app.services.search import search_similar

def main():
    qvec = get_embedding("что такое векторы")
    rows = search_similar(qvec, top_k=5)
    print("rows:", len(rows))
    for r in rows:
        print(r["chunk_id"], f"{r['distance']:.6f}", r["content"][:80])

if __name__ == "__main__":
    main()
