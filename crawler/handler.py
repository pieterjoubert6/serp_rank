def save_rankings(rank_data, category_definitions, latest_ranks):
    # file2write = open("thedata.txt", 'w')
    # for item in rank_data['ranks']['US']:
    #     print(item)
    #     if item.get('category') is None:
    #         item['category'] = 0
    #     item['category_name'] = category_definitions[item['category']]
    #     rank = Rank(date=date.fromisoformat(item["date"]), rank=item["rank"], db=item["db"],
    #                 category=category if (category := item.get("category")) else 0)
    #     session.add(rank)
    #     file2write.write(str({
    #         "date": item["date"],
    #         "rank": item["rank"], "db": item["db"],
    #         "category": category if (category := item.get("category")) else 0}))
    # file2write.close()
    file2write = open("metrics", 'w')
    for item in latest_ranks:
        print(item)
        # latest_rank = LatestRank(
        #     rank=item["rank"],
        #     category=item["category"],
        #     category_name=item["category_name"],
        #     date=date.today()
        # )
        # session.add(latest_rank)

        # file2write.write(str({
        #     # "date": date.today(),
        #     "rank": item["rank"],
        #     # "db": item["db"],
        #     "category": item["category"],
        #     "category_name": item["category_name"]
        # }))

        file2write.write(
            f'serp_rank{{category="{item["category"]}",category_name="{item["category_name"]}"}} {item["rank"]} \n'
        )

        # session.commit()
    file2write.close()
