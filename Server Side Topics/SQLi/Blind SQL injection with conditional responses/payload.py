def determine_response_length(inner_query, url, no_proxy=False):
    log.info("Determining response length for query.")
    sess = requests.Session()
    for i in range(1, 5):
        outer_query = format_length_query(inner_query, i)
        