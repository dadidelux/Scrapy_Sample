from curl_cffi import requests as curl_requests
import pandas as pd
import time

# Free People API endpoint for women's clothes (discovered via network tab)
API_URL = "https://www.freepeople.com/api/v1/product/search/"

params = {
    "q": "",
    "category": "womens-clothes",
    "page": 1,
    "limit": 120,  # max per page
}

all_products = []

# Paste your browser cookies for freepeople.com here (from Chrome DevTools > Application > Cookies)
COOKIES = "SSLB=1; urbn_inventory_pool=INTL_DIRECT; urbn_language=en-US; urbn_currency=USD; siteId=fp-us; urbn_geo_region=AS-SG; urbn_channel=web; urbn_clear=true; urbn_tracer=NN9LYALM8L; urbn_edgescape_site_id=fp-us; urbn_data_center_id=US-NV; urbn_country=PH; urbn_uuid=1b96ddaf-3340-4892-8f23-6ba5c19ffda2; urbn_site_id=fp-us; urbn_device_info=web%7Cother%7Cdesktop; pxcts=443464e7-3c6c-11f0-8c2f-5511e048e364; _pxvid=419c67d4-3c6c-11f0-b431-5bb4470488b1; __pxvid=44929081-3c6c-11f0-9c3b-124267abd349; split_tag_control=Conversant; utag_main_marketing_split_test=eps; cebs=1; _gcl_gs=2.1.k1$i1748509611$u154250991; _gcl_au=1.1.1001837175.1748509621; utag_main_v_id=01971b4b7ac40083e138ffab7f600506f00f406700c48; _ce.clock_data=2396%2C152.32.96.10%2C1%2C0e0369e2813db7deb26e5937c353aab4%2CChrome%2CPH; __spdt=6324d10e485844789a96dc392c9fd91f; _ga=GA1.1.1388356382.1748509622; __attentive_id=1ed192834da14508869e701a947f0a02; __attentive_cco=1748509621692; smartDash=845c76e4-e8ba-4961-8dd6-c2c2e4182159; _scid=mhPye4R1ytpnaH4IE_bjjZUovvqs_ouS; _fbp=fb.1.1748509622033.307046966383832764; _pin_unauth=dWlkPU9UWXhOak5pWWpNdFlUY3hOUzAwTXpJMkxXRmlNMkl0TnpCak5HWmpOakZpTVROaw; _tt_enable_cookie=1; _ttp=01JWDMQ01S3N7VA583JK3PPVFF_.tt.1; _ScCbts=%5B%2296%3Bchrome.2%3A2%3A5%22%5D; __attentive_dv=1; _li_dcdm_c=.freepeople.com; _lc2_fpi=8188ef299b6c--01jwdmq15ckj5q0tbgkysa0zpa; _lc2_fpi_js=8188ef299b6c--01jwdmq15ckj5q0tbgkysa0zpa; _gcl_aw=GCL.1748509640.Cj0KCQjwucDBBhDxARIsANqFdr1gNvmPvbEyyFegxZ7dSLqMxDF2JI31iPp72Rm7-Fl0fG_IH0jUNQMaAlE7EALw_wcB; _gcl_dc=GCL.1748509640.Cj0KCQjwucDBBhDxARIsANqFdr1gNvmPvbEyyFegxZ7dSLqMxDF2JI31iPp72Rm7-Fl0fG_IH0jUNQMaAlE7EALw_wcB; BVBRANDID=c4e26b89-6cad-45e2-a637-5d9a16274de1; dtm_token=AQAEERt3yZAm4wEBAQEsAQA8wAABAQCWGmWjQgEBAJYaZaNC; _svsid=1b170a69d44f49bc66b170c5546d515a; urbn_page_visits_count=%7B%22fp-us%22%3A7%7D; __attentive_ss_referrer=https://www.freepeople.com/shop/we-the-free-good-luck-mid-rise-barrel-jeans/?category=SEARCHRESULTS&color=105&searchparams=q=93748200&type=REGULAR&quantity=1; SS_SHOP_THE_LOOK_VARIANT=0; ss-enable-bisn-confirmation=1; SS_Qualtrics_Load=1; urbn_auth_payload=%7B%22authToken%22%3A%22eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJmcCIsImV4cCI6MTc0ODUxNzI5NS40MTQ1MDk4LCJpYXQiOjE3NDg1MTY2OTUuNDE0NTA5OCwiZGF0YSI6IntcImNyZWF0ZWRUaW1lXCI6IDE3NDg1MDk2MTAuNDA0MDM0MSwgXCJwcm9maWxlSWRcIjogXCJYVENFaVVpVmlibFN1MTdKcG9wbTRDa1M1NGYxdkp0TnBLaFZiSkN1aHg0KytkU0taWVhYODB4QnhTWGV1MWxMNVUrM3JzMnJ4aGptNHBEMzBDY0lCdz09ODVjOGVhYmRiYTM3Yjc4OGM3ZGIyZTlhNmU1OWM2YzZkYzBkMTMxNGQxYTY4NDc4MDUxNzdlYTBjZWQyZmUyZVwiLCBcImFub255bW91c1wiOiB0cnVlLCBcInRyYWNlclwiOiBcIk5OOUxZQUxNOExcIiwgXCJzY29wZVwiOiBbXCJHVUVTVFwiXSwgXCJzaXRlSWRcIjogXCJmcC11c1wiLCBcImJyYW5kSWRcIjogXCJmcFwiLCBcInNpdGVHcm91cFwiOiBcImZwXCIsIFwiZGF0YUNlbnRlcklkXCI6IFwiVVMtTlZcIiwgXCJnZW9SZWdpb25cIjogXCJBUy1TR1wiLCBcImVkZ2VzY2FwZVwiOiB7XCJyZWdpb25Db2RlXCI6IFwiMDBcIn0sIFwiY2FydElkXCI6IFwieXN0Uk9mTW54RmFmMWFkWkdWNnBHZk42eXFLczkxZ3lwdVZ0a1JvcW9wQnBwbjJjLzRoVU9aeElYUHp0SDBJNTVVKzNyczJyeGhqbTRwRDMwQ2NJQnc9PTJjZGFlNDFlMjE0OGI5OWI3Yzg5N2YwNDNkZWI1NGMyMTUzYjMyZWZmODA2ZDI1Y2UwMDJhN2Q2NGNkZTg0MWNcIn0ifQ.RGdl8jrx9OagitHGOvi7a6VefDY9UavJRO6cRXREcuA%22%2C%22reauthToken%22%3A%22eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJmcCIsImV4cCI6MTc2NDA2ODY5NS40MTQ5MTcyLCJpYXQiOjE3NDg1MTY2OTUuNDE0OTE3MiwiZGF0YSI6IntcImNyZWF0ZWRUaW1lXCI6IDE3NDg1MTY2OTUuNDE0OTAwMywgXCJzY29wZVwiOiBbXCJHVUVTVFwiXSwgXCJ0cmFjZXJcIjogXCJOTjlMWUFMTThMXCIsIFwicHJvZmlsZUlkXCI6IFwiWFRDRWlVaVZpYmxTdTE3SnBvcG00Q2tTNTRmMXZKdE5wS2hWYkpDdWh4NCsrZFNLWllYWDgweEJ4U1hldTFsTDVVKzNyczJyeGhqbTRwRDMwQ2NJQnc9PTg1YzhlYWJkYmEzN2I3ODhjN2RiMmU5YTZlNTljNmM2ZGMwZDEzMTRkMWE2ODQ3ODA1MTc3ZWEwY2VkMmZlMmVcIn0ifQ.WENZlnQB4lSJgDYOpBLFKZbmNKxCiPtWkZlfMXKiF3Y%22%2C%22reauthExpiresIn%22%3A15552000%2C%22expiresIn%22%3A600%2C%22scope%22%3A%22GUEST%22%2C%22tracer%22%3A%22NN9LYALM8L%22%2C%22dataCenterId%22%3A%22US-NV%22%2C%22geoRegion%22%3A%22AS-SG%22%2C%22edgescape%22%3A%7B%22regionCode%22%3A%2200%22%2C%22country%22%3A%22US%22%2C%22city%22%3A%22Seattle%22%2C%22zipCodes%22%3A%2298160%22%7D%2C%22trueClientIp%22%3A%2294.140.8.17%22%2C%22createdAt%22%3A1748516695418%2C%22authExpiresTime%22%3A1748517175.418%2C%22reauthExpiresTime%22%3A1764068695.418%7D; SSID_BE=CQB_6h1GAAAAAACqIzho0TvAKKojOGgCAAAAAADWwBJqVz84aADRnJFdAQOgmSoAqiM4aAIAUFwBAdJ-KgBZPzhoAQCtVAEDfcUpAKojOGgCAGtYAQPnICoAqiM4aAIAAl0BA1yOKgCqIzhoAgA; SSSC_A15=513.G7509791592375401425.2|87213.2737533:88171.2760935:89168.2784978:89346.2788956:89489.2791840; _pxhd=7EcedAtOZR99qVNl/IaYkauPt4LwKyG0J5pbVSkE2cNYcG3ZwLDaRBGnGdUO2xblgmgh1nT/CFeAW07PFLoMOQ==:XyANOAoD7//6mCVI/jCCwXAlcv1tJQ6adUwiq3AkJQGk/DijvYmNlZWsbruHyw5D6Qkhr0WslnWQqZNf394frBZYwWD/QbfnxauYCdPNJsw=; utag_main__sn=2; utag_main_ses_id=1748516702723%3Bexp-session; utag_main__pn=1%3Bexp-session; utag_main_isLoggedIn=false%3Bexp-session; utag_main_tag_session_835=1%3Bexp-session; utag_main__ss=0%3Bexp-session; utag_main__se=3%3Bexp-session; utag_main__st=1748518503272%3Bexp-session; _uetsid=481491903c6c11f094c2b12b92a34e61|2bsorx|2|fwb|0|1975; _rdt_uuid=1748509621068.6fc68f3d-8794-48ce-81e7-82a006853e58; __attentive_session_id=6af38f43561f4b43b0001927da012ddb; _attn_=eyJ1Ijoie1wiY29cIjoxNzQ4NTA5NjIxNjkwLFwidW9cIjoxNzQ4NTA5NjIxNjkwLFwibWFcIjoyMTkwMCxcImluXCI6ZmFsc2UsXCJ2YWxcIjpcIjFlZDE5MjgzNGRhMTQ1MDg4NjllNzAxYTk0N2YwYTAyXCJ9Iiwic2VzIjoie1widmFsXCI6XCI2YWYzOGY0MzU2MWY0YjQzYjAwMDE5MjdkYTAxMmRkYlwiLFwidW9cIjoxNzQ4NTE2NzA0MDkyLFwiY29cIjoxNzQ4NTE2NzA0MDkyLFwibWFcIjowLjAyMDgzMzMzMzMzMzMzMzMzMn0ifQ==; _scid_r=rJPye4R1ytpnaH4IE_bjjZUovvqs_ouS3u7wxQ; ttcsid=1748516704251::G-dsXqqjnzjyYd9SdwhN.2.1748516704251; utag_main_dc_visit=2; utag_main_dc_event=1%3Bexp-session; _tq_id.TV-6309096327-1.d0d5=6ec50e60b05ad467.1748509621.0.1748516704..; __attentive_pv=4; _clsk=; _clck=; _ce.s=v~d21756e81a02051260c9cbb163d00f2d5d26b4ea~lcw~1748512092642~vir~new~lva~1748509620265~vpv~0~v11.cs~252616~v11.s~4812ede0-3c6c-11f0-8b1d-d9d926bb4f55~v11.vs~d21756e81a02051260c9cbb163d00f2d5d26b4ea~v11.ss~1748509621186~v11ls~4812ede0-3c6c-11f0-8b1d-d9d926bb4f55~lcw~1748516704465; cebsp_=27; ttcsid_C4RSTB16H18A0MH16H6G=1748516704250::HsrkhW-ZWQGRQiESMxtD.2.1748516704596; _uetvid=48149f503c6c11f0998465c1dae85ec0|th8hi7|1748516704774|3|1|bat.bing.com/p/insights/c/q; utag_main_dc_region=us-west-2%3Bexp-session; MGX_UC=JTdCJTIyTUdYX1AlMjIlM0ElN0IlMjJ2JTIyJTNBJTIyOTBjODA2YzItMzNjYS00NmRkLWFjOGItZWU3YzA3YTJmNjg0JTIyJTJDJTIyZSUyMiUzQTE3NDkwNDIzMDM4MzAlN0QlMkMlMjJNR1hfQ0lEJTIyJTNBJTdCJTIydiUyMiUzQSUyMmNlODc3N2ZiLWJhMjEtNGQyZC1iMDFiLTM0OTRkMjQ1NzA3YyUyMiUyQyUyMmUlMjIlM0ExNzQ5MDQyMzAzODMyJTdEJTJDJTIyTUdYX1BYJTIyJTNBJTdCJTIydiUyMiUzQSUyMjA2ODExNjEzLTFmMjItNDEzNC05NzhlLWJkM2ZmY2YxNTFlZiUyMiUyQyUyMnMlMjIlM0F0cnVlJTJDJTIyZSUyMiUzQTE3NDg1MTg1MDY0ODIlN0QlMkMlMjJNR1hfVlMlMjIlM0ElN0IlMjJ2JTIyJTNBMSUyQyUyMnMlMjIlM0F0cnVlJTJDJTIyZSUyMiUzQTE3NDg1MTg1MDY0ODIlN0QlMkMlMjJNR1hfRUlEJTIyJTNBJTdCJTIydiUyMiUzQSUyMm5zX3NlZ18wMDclMjIlMkMlMjJzJTIyJTNBdHJ1ZSUyQyUyMmUlMjIlM0ExNzQ4NTE4NTA2NDgyJTdEJTdE; utag_main_ttd_uuid=f5866608-cd88-447f-a436-bd6f15016f62%3Bexp-session; utag_main_cms_835=1%3Bexp-session; OptanonConsent=isGpcEnabled=0&datestamp=Thu+May+29+2025+19%3A06%3A46+GMT%2B0800+(Philippine+Standard+Time)&version=202403.1.0&browserGpcFlag=0&isIABGlobal=false&identifierType=Cookie+Unique+Id&hosts=&consentId=1b96ddaf-3340-4892-8f23-6ba5c19ffda2&interactionCount=1&isAnonUser=1&landingPath=https%3A%2F%2Fwww.freepeople.com%2Fwomens-clothes%2F&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1; SSRT_A15=xD84aAADAA; _ga_PDBRPFW49G=GS2.1.s1748516699$o2$g1$t1748516807$j59$l0$h0; _px3=c7eb54d8e7538d964ee2266a66a5940cec7aff08cdb9239a8abc6d7629c9f818:5+9ok+C7EeBqw/CW/L5FSwcYvxu0Zv62KkyfPCgCIcl4I7uRK4ehrCjz2TGT6iPVOScL3uZxJdZSHY668gjUXA==:1000:SXTeEO+jyIRnq++EvKk6jJRKJXW0uR6rUjbWeCwXrQhCqjUqhWr71B1V/+kSZNkny2+Cqj86LKRnom5fDL9j3kFtMjDkKkHgBIm5BDqt+F/WSn9H84zhw12NAMQ4kJhMGFDAxRHCE0zmxEWVg3b+Y2S7Z78AEO33VS3SDogyHH9Wua98mIFOK1tB3mgOkijOgzax/mkDCtN3Oy4sl3LnWI3oOU8vl7QR/T6hAtQazRQ="

while True:
    resp = curl_requests.get(
        API_URL,
        params=params,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.freepeople.com/womens-clothes/",
            "Connection": "keep-alive",
            "Origin": "https://www.freepeople.com",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Cookie": COOKIES,
        },
        impersonate="chrome"
    )
    try:
        data = resp.json()
    except Exception as e:
        print(f"[ERROR] Could not decode JSON on page {params['page']}")
        print(f"Status code: {resp.status_code}")
        print(f"First 500 bytes of response:\n{resp.content[:500]!r}")
        print(f"Exception: {e}")
        break
    products = data.get("products", [])
    if not products:
        break
    for p in products:
        all_products.append({
            "title": p.get("displayName"),
            "price": p.get("price", {}).get("current"),
            "url": f"https://www.freepeople.com{p.get('url', '')}",
            "sku": p.get("sku"),
            "brand": p.get("brand"),
            "image": p.get("defaultImageUrl"),
        })
    print(f"Fetched page {params['page']}: {len(products)} products")
    if not data.get("hasMore", False):
        break
    params["page"] += 1
    time.sleep(1)

# Save to CSV
pd.DataFrame(all_products).to_csv("freepeople_products_api.csv", index=False)
print(f"✅ Saved {len(all_products)} products to freepeople_products_api.csv")
