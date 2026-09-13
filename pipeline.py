from agents import build_reader_agent,build_search_agent, writer_chain, critic_chain

def run_research_pipeline(topic : str) -> dict:
    state = {}
    # Search Agent working
    print("\n", "="*50)
    print("Step 1 - Search agent working ...")
    print("="*50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages" : [("user",f"Find recent, reliable and detailed information about : {topic}")]
    })
    state["search_result"] = search_result['messages'][-1].content
    print("\n Search result : " , state['search_result'])


    # Step 2 reader Agent 
    print("\n", "="*50)
    print("Step 2 - Reader agent is Scraping top resources ...")
    print( "="*50)

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
                      f"Based on the following search results about '{topic}',"
                      f"pick the most relevant URL and scrape it for deeper content. \n\n"
                      f"Search Results : \n{state['search_result'][:800]}"
                      )]
    })

    state['scrapped_result'] = reader_result['messages'][-1].content
    print("\n  Scraped Content \n",state['scrapped_result'])

    # Step 3 -> Writer Chain 
    print("\n", "="*50)
    print("Step 3 - Writeris drafting the report ...")
    print("="*50)

    research_combined = (
        f"SEARCH RESULTS : \n {state['search_result']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scrapped_result']} \n\n"
    )

    state['report'] = writer_chain.invoke({
        "topic" : topic,
        "research" : research_combined
    })

    print("\n Final Report \n {state['report']}")

    # Critic Report
    print("\n", "="*50)
    print("Step 4 - critic is reviewing the report ...")
    print( "="*50)

    state['feedback'] = critic_chain.invoke({"report" : state['report']})
    print("\n Critic report \n",state['feedback'])

    return state


if __name__ == "__main__":
    topic = input("\n Enter a Research Topic : ")
    run_research_pipeline(topic)