
query = "which city has the largest population in the world?"

# create the query vector
xq = pc.inference.embed(
    model=model_name,
    inputs=[query],
    parameters={
        "input_type": "query",
        "truncate": "END"
    }
).data[0]['values']

# now query
xc = index.query(vector=xq, top_k=5, include_metadata=True)
xc