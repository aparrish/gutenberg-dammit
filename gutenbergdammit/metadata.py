# code based on/adapted from https://github.com/julianbrooke/GutenTag
# Creative Commons Attribution-ShareAlike 4.0 International

import codecs
from collections import defaultdict

def fix_year(year_string):
    year_string = year_string.replace("?", "")
    year_string = year_string.replace("AD", "")
    if "BC" in year_string:
        BC = True
        year_string = year_string.replace("BC"," ")
    else:
        BC = False
    try:
        year = int(year_string)
        if BC:
            year = -year
    except:
        year = "?"
    return year

class MetadataReader:

    wanted_tags = set(["Author","Title", "LoC Class", "Subject", "Language",
        "Copyright Status"])

    def get_metatag_contents(self,html,tag):
        index = html.find('<th scope="row">%s</th>' % tag)
        result = []
        while index != -1:
            result.append(html[html.find("<td>",index) + 4 :html.find(
                "</td>", index)].replace("&amp;","&"))
            index = html.find('<th scope="row">%s</th>' % tag, index + 1)
        return result

    def expand_author(self,tags):
        if "Author" not in tags:
            return
        authors = tags["Author"]
        tags["Author"] = []
        tags["Author Birth"] = []
        tags["Author Death"] = []
        tags["Author Given"] = []
        tags["Author Surname"] = []
        for author in authors:
            parts = author.split(", ")
            birth = None
            death = None
            given = None
            surname = None
            if len(parts) >= 2:
                if parts[-1].count("-") == 1:
                    birth_string, death_string = parts[-1].split("-")
                    birth = fix_year(birth_string)
                    death = fix_year(death_string)
                    parts = parts[:-1]
                parts.reverse()
                author = " ".join(parts)
                if len(parts) == 2:
                    given = parts[0]
                    surname = parts[1]
                    found_names = True

            if given:
                tags["Author Given"].append(given)
            else:
                tags["Author Given"].append("?")
            if surname:
                tags["Author Surname"].append(surname)
            else:
                tags["Author Surname"].append("?")            
            if birth:
                tags["Author Birth"].append(birth)
            else:
                tags["Author Birth"].append("?")
            if death:
                tags["Author Death"].append(death)
            else:
                tags["Author Death"].append("?")

            tags["Author"].append(author)

    def get_href_and_charset(self,html_text):
        index = html_text.find("text/plain")
        if index == -1:
            return None,-1
        index = html_text.find('charset="', index)
        if index == -1:
            charset = "utf-8"
            index = html_text.find("text/plain")
        else:            
            charset = html_text[index + 9:html_text.find('"',index + 9)]
        index = html_text.find(' href="', index)
        if index == -1:
            href = None
        else:
            href = html_text[index + 9:html_text.find('"',index + 9)]

        return href, charset

    def get_PG_metadata(self,filename):
        f = codecs.open(filename, encoding="utf-8")
        html_text = f.read()
        f.close()
        tag_dict = {}
        for tag in self.wanted_tags:
            tag_dict[tag] = self.get_metatag_contents(html_text,tag)
        self.expand_author(tag_dict)
        for i in range(len(tag_dict["Title"])):
            tag_dict["Title"][i] = tag_dict["Title"][i].replace("\n","\t")
        href, charset = self.get_href_and_charset(html_text)
        return href,charset,tag_dict


class MetadataReaderRDF:

    title_remove = ["&#13;"]

    language_lookup = {
            "en":"English",
            "fr":"French",
            "es":"Spanish",
            "de":"German",
            "pt":"Portuguese",
            "ja":"Japanese",
            "zh":"Chinese",
            "ru":"Russian",
            "ar":"Arabic",
            "pl":"Polish",
            "it":"Italian",
            "el":"Greek",
            "he":"Hebrew",
            "ko":"Korean",
            "hi":"Hindi",
            "la":"Latin",
            "nl":"Dutch",
            "sv":"Swedish",
            "no":"Norweigan",
            "fi":"Finnish"}

    def get_PG_metadata(self,filename):
        f = codecs.open(filename, encoding="utf-8")
        tag_dict = defaultdict(list)
        in_subject = False
        in_creator = False
        add_next_line_to_title = False
        encodings = []
        for line in f:
            if add_next_line_to_title:
                if "<" in line:
                    end_index = line.find("<")
                    add_next_line_to_title = False
                else:
                    end_index = -1
                tag_dict["Title"][-1] += "\t" + line[:end_index]
                
            if "<dcterms:creator>" in line:
                in_creator = True
                full_name = None
                birth_year = None
                death_year = None
                first_name = None
                last_name = None
            elif "</dcterms:creator>" in line:
                if full_name:
                    tag_dict["Author"].append(full_name)
                    tag_dict["Author Birth"].append(birth_year)
                    tag_dict["Author Death"].append(death_year)
                    tag_dict["Author Given"].append(first_name)
                    tag_dict["Author Surname"].append(last_name)

            elif in_creator and "<pgterms:name>" in line:
                start_index = line.find(">") + 1
                end_index = line.find("<",start_index)
                name = line[start_index:end_index]
                #if "(" in name:
                #    name = name[:name.find(" (")]
                stuff = name.split(', ')
                if len(stuff) == 2:
                    first_name = stuff[1]
                    last_name = stuff[0]
            
                stuff.reverse()
                full_name = " ".join(stuff)
                #print full_name
            elif in_creator and "pgterms:birthdate" in line:
                start_index = line.find(">") + 1
                end_index = line.find("<",start_index)
                birth_year = line[start_index:end_index]
                birth_year = fix_year(birth_year)
            elif in_creator and "pgterms:deathdate" in line:
                start_index = line.find(">") + 1
                end_index = line.find("<",start_index)
                death_year = line[start_index:end_index]
                death_year = fix_year(death_year)
            elif "<dcterms:subject>" in line:
                in_subject = True
                value = None
                is_LLC = False
            elif "</dcterms:subject>" in line:
                in_subject = False
                if value:
                    if is_LLC:
                        tag_dict["LoC Class"].append(value)
                    else:
                        tag_dict["Subject"].append(value)
            elif in_subject and "<rdf:value>" in line:
                start_index = line.find(">") + 1
                end_index = line.find("<",start_index)
                value = line[start_index:end_index]
            elif in_subject and '<dcam:memberOf rdf:resource="http://purl.org/dc/terms/LCC"/>' in line:
                is_LLC = True
            elif "<pgterms:file" in line and ".txt" in line:
                if "-8" in line:
                    encodings.append("latin-1")
                elif "-0" in line:
                    encodings.append("utf-8")
                else:
                    encodings.append("us-ascii")
            elif "<dcterms:title>" in line:
                start_index = line.find(">") + 1
                end_index = line.find("<",start_index)
                if end_index == -1:
                    add_next_line_to_title = True
                tag_dict["Title"].append(line[start_index:end_index])
            elif "<dcterms:rights>" in line:
                start_index = line.find(">") + 1
                end_index = line.find("<",start_index)
                tag_dict["Copyright Status"] = [line[start_index:end_index]]
            elif "RFC4646" in line:
                start_index = line.find(">") + 1
                lang = line[start_index:start_index + 2]
                if lang in self.language_lookup:
                    tag_dict["Language"].append(self.language_lookup[lang])
                else:
                    tag_dict["Language"].append("Other")
        f.close()
        if "us-ascii" in encodings:
            charset = "us-ascii"
        elif "latin-1" in encodings:
            charset = "latin-1"
        else:
            charset = "utf-8"
        href = "/sup_gut/" + filename.split("/")[-1][:-3] + "zip"
        if "Title" not in tag_dict:
            tag_dict["Title"].append("?")
        for i in range(len(tag_dict["Title"])):
            for to_remove in self.title_remove:
                tag_dict["Title"][i] = tag_dict["Title"][i].replace(to_remove,"")
        return  href,charset,tag_dict

