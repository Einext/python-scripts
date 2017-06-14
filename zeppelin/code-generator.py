import json
import sys

def toJson(path):
    with open(path, "r", encoding= "utf-8-sig") as f:
        content = f.read()
        return json.loads(content)


def parseParagraph(p):
    # result = p["result"]
    # code = result["code"]
    # output = result["msg"]
    # status = p["status"]
    # started = p["dateStarted"]
    # finished = p["dateFinished"]
    # pid = p["id"]
    text = ""
    if "text" in p:
      text = p["text"] + "\n"
    return text

def writeToFile(codes, output_path):
    with open(output_path, "w") as f:
        f.writelines(codes)

if __name__ == "__main__":
    if not len(sys.argv) is 3:
        print("Usage: python3 zeppeline-stat.py <input notebook.json> <output .scala>")
        sys.exit("Invalid arguments")

    path = sys.argv[1]
    print("Path: ", path)
    output_file = sys.argv[2]
    print("Output file", output_file)
    j = toJson(path)
    codes = [parseParagraph(p) for p in j["paragraphs"]]
    codes = [code for code in codes if not code.startswith("%")]
    writeToFile(codes, output_file)
