import pickle
import os
import bs4
import pandas as pd

# initialize main Data Frame
column_headers = ["url", "title", "location", "date_str", "prize", "cbj_percentage", "champ_bool",
                  "overall", "chicken", "ribs", "pork", "brisket"]
data = pd.DataFrame(columns=column_headers)

directory = "contest_html"
for i, fn in enumerate(os.listdir(directory)):
    if fn.endswith(".html"):
        fnj = directory + "/" + fn
        with open(fnj, 'rb') as fc:
            contest = bs4.BeautifulSoup(fc)

        row_dict = {"url": "NA", "title": "NA", "location": "NA", "date_str": "NA", "prize": "NA",
                    "cbj_percentage": "NA", "champ_bool": "NA", "overall": "NA",
                    "chicken": "NA", "ribs": "NA", "pork": "NA", "brisket": "NA"}

        # url
        url = "http://www.kcbs.us/event/" + fn[:4] + "/" + fn[5:-5]
        row_dict["url"] = url

        # title
        title_handle = contest.select(".event_head")
        if len(title_handle) > 0:
            title = title_handle[0].text.strip()
            row_dict["title"] = title

        # location / date
        sub_head = contest.select("#event_subhead")
        if len(sub_head) > 0:
            sub_head = sub_head[0]
            sub_head = sub_head.text.split('\n\t\t')
            if len(sub_head) == 3:
                location = sub_head[1].strip()
                date_str = sub_head[2].strip()
                row_dict["location"] = location
                row_dict["date_str"] = date_str

        # Meta Data
        meta_dict = {"website": "NA", "kcbs reps": "NA", "contest number": "NA", "prize money": "NA",
                     "cbj percentage": "NA"}
        p_tags = contest.select("p")
        for tag in p_tags:
            text = tag.text
            if "Contest Number:" in text:
                meta_data = text.split("\n")
                for line in meta_data:
                    line = line.split(":")
                    if len(line) == 2:
                        key = line[0].strip().lower()
                        value = line[1].strip()
                        if key == "prize money":
                            value = float(value[1:].replace(",",""))
                        meta_dict[key] = value

        row_dict["prize"] = meta_dict["prize money"]
        row_dict["cbj_percentage"] = meta_dict["cbj percentage"]

        # State Championship Boolean
        champ_text = contest.select('.float20 p strong em')
        champ_bool = False
        if len(champ_text) > 0:
            if champ_text[0].text.strip() == "STATE CHAMPIONSHIP":
                champ_bool = True
        row_dict["champ_bool"] = champ_bool

        # Contest Result DataFrames
        df_dict = {"overall": "NA", "chicken": "NA", "ribs": "NA", "pork": "NA", "brisket": "NA"}
        valids = df_dict.keys()
        sub_cols = ["place", "name", "score"]
        result_html = contest.select("div.grid07.float20 table.contestResults")
        if len(result_html) > 0:
            # for each table of results (overall, chicken, ribs, pork, brisket)
            for tbl in result_html:
                rows = tbl.select('tr')
                if len(rows) > 0:
                    # name the table by its header column
                    table_name = rows[0].text.lower().strip()
                    if table_name == "pork ribs":
                        table_name = "ribs"
                    if table_name in valids:
                        df_dict[table_name] = pd.DataFrame(columns=sub_cols)
                        # for each row in each table
                        for q in range(1, len(rows)):
                            row = rows[q]
                            # unpack cells from row
                            cells = row.select("td")
                            if len(cells) == 3:
                                place = float(cells[0].text)
                                team_name = cells[1].text
                                score = float(cells[2].text)
                                # add the row to the dataframe (in the dictionary)
                                new_result_row = [place, team_name, score]
                                df_dict[table_name].loc[-1] = new_result_row
                                df_dict[table_name].index = df_dict[table_name].index + 1
        for key in valids:
            row_dict[key] = df_dict[key]

        # Insert into table
        data.loc[-1] = row_dict
        data.index = data.index + 1

        print "Completed:", i

    else:
        print "Non-HTML file detected!"
        print fn
        break

with open('pkls/contest_data.pkl', 'wb') as f:
    pickle.dump(data, f)