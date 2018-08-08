# code based on/adapted from https://github.com/julianbrooke/GutenTag
# Creative Commons Attribution-ShareAlike 4.0 International

import re

class TextCleaner:
    junk_indicators = ("project gutenberg"," etext"," e-text",
                        "http:","distributed proofreading",
                        "distributed\nproofreading", " online"
                        "html","utf-8","ascii","transcriber's note",
                        "scanner's note", "\\.net","\\.org","\\.com",
                        "\\.edu","www\\.", "electronic version",
                        " email","\\.uk","digitized", "\n\nproduced by",
                        "david reed", "\ntypographical errors corrected",
                        "\[note: there is a","etext editor's","u.s. copyright",
                        "\nerrata"," ebook"," e-book",
                        "author:     ","</pre>", "\[end of","internet archive")
                
    
    def clean_text(self,text):
        text = text.replace("\r\n","\n").replace("\r","\n") # normalize lines
        # get rid of explicit section breaks
        text = re.sub("\n[ *-]+\n","\n\n",text)
        #text = re.sub("\[Illustration:?[^\]]*\]","",text)
        text = re.sub("<<[^>]+>>","",text)
        text = re.sub("[^_]_______________________________________.*_________________________________[^_]","\n\n",text)
        lower_text = text.lower()
        all_junk_indicies = [0, len(text)]
        for junk_indicator in self.junk_indicators:
            all_junk_indicies.extend([m.start() for m in re.finditer(junk_indicator,lower_text)])
        all_junk_indicies.sort()
        best_points = None
        best_length = 0
        for i in range(len(all_junk_indicies) - 1):
            if all_junk_indicies[i+1] - all_junk_indicies[i] > best_length:
                best_points = [all_junk_indicies[i],all_junk_indicies[i+1]]
                best_length = all_junk_indicies[i+1] - all_junk_indicies[i]
        found = False
        best_length = float(best_length)
        if best_length < 5000: # too small for general method to work reliably
            m = re.search("end of [^\\n]*project gutenberg",lower_text)
            if m:
                best_points[1] = m.start()
                i = 0
                while all_junk_indicies[i] < best_points[1] - 100:
                    i += 1
                best_points[0] = all_junk_indicies[i-1]
            else:
                return ""

        i = 4
        while not found:
            looking_for = "\n"*i
            result = text.find(looking_for, best_points[0])
            if result != -1 and ((best_points[1] - result)/best_length > 0.98 or i == 1):
                found = True
            i -= 1

        return text[result:text.rfind("\n", 0, best_points[1])].strip()

