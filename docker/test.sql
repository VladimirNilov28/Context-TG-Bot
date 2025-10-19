SELECT 
  c.id, 
  left(c.content, 80) AS preview, 
  (e.embedding <=> CAST(e.embedding AS vector)) AS dist
FROM embeddings e
JOIN chunks c ON c.id = e.chunk_id
LIMIT 3;
