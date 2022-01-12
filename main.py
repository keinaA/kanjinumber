import flask

# int型の数値を1桁ずつ配列に格納して返す関数
def digit(i):
    if i > 0:
        return digit(i//10) + [i%10]
    else:
        return []

# 4桁の数字を漢数字に変換する関数        
def until_thousand_number2kanji(tmp_numbers_length , tmp_output_str, tmp_split_list):
    # 上の桁（千の位）から1桁ずつ処理を行う
    while tmp_numbers_length  > -1:
        # 数字が1桁の時（一の位）
        if tmp_numbers_length  == 0 and tmp_split_list[tmp_numbers_length ] != 0:
            # その数字を漢数字に変換したものをtmp_output_strに足す
            tmp_output_str += numbers_directory[tmp_split_list[0]]
            tmp_numbers_length  = -1
            
        # 数字が2桁の時（十の位）
        elif tmp_numbers_length  == 1 and tmp_split_list[tmp_numbers_length] != 0:
            # 一番最後の桁が0なら最後の1桁は出力しない
            if tmp_split_list[0] == 0:
                # 十の位を漢数字に変換したもの+「十」をtmp_output_strに足す
                tmp_output_str += numbers_directory[tmp_split_list[tmp_numbers_length]] + digits_directory[10 ** tmp_numbers_length]
            # そうでないなら、最後の1桁を出力する
            else:
                # 十の位を漢数字に変換したもの+「十」+一の位を漢数字に変換したものをtmp_output_strに足す
                tmp_output_str += numbers_directory[tmp_split_list[tmp_numbers_length]] + digits_directory[10 ** tmp_numbers_length] + numbers_directory[tmp_split_list[0]]
            tmp_numbers_length  = -1
        
        # 数字が3.4桁の時（百、千の位）
        elif (tmp_numbers_length  == 2 or tmp_numbers_length  == 3) and tmp_split_list[tmp_numbers_length ] != 0:
            # 百の位（千の位）を漢数字に変換したもの+「百（千）」をtmp_output_strに足す
            tmp_output_str += numbers_directory[tmp_split_list[tmp_numbers_length ]] + digits_directory[10 ** tmp_numbers_length ]
            tmp_numbers_length  -= 1
        else:
            tmp_numbers_length  -= 1
    # 4桁の漢数字を返す
    return tmp_output_str

# 0～9の変換表
numbers_directory = {
    0: '零',
    1: '壱',
    2: '弐',
    3: '参',
    4: '四',
    5: '五',
    6: '六',
    7: '七',
    8: '八',
    9: '九',
}

# 10,100,1000の変換表
digits_directory = {
    10: '拾',
    100: '百',
    1000: '千'
}

# 万、億、兆の変換表
large_digits_directory = {
    10000: '万',
    100000000: '億',
    1000000000000: '兆'
}

app = flask.Flask(__name__)

@app.route("/", methods=["GET"])
def hello():
    return "[/v1/number2kanji/<半角数字か全角数字>]で、アラビア数字を漢数字に変換できます"

# アラビア数字を漢数字に変換するAPI
@app.route("/v1/number2kanji/<input>", methods=["GET"])
def number2kanji(input):
    input_list = [] # 入力された数字を格納する配列
    output_str = '' # 出力用の文字列
    int_input = 0   # 入力された数値を格納する

    # もし、入力が全角数字か半角数字ならばint型に変換する
    if input.isdigit():
        int_input = int(input)
    # 全角数字、半角数字以外ならば204を返して、処理を終了する
    else:
        return 204
    
    # 入力が「0」じゃないとき、変換するための処理を行う
    if int_input != 0:
        # 入力された数値を1桁ずつ、配列に格納
        input_list = digit(int_input)
    
    # 入力された数値の配列の順番を逆にして、reverse_listに格納する
    reverse_list = list(reversed(input_list))
    #配列の長さをlist_lengthに格納する
    list_length = len(input_list)

    # もし0じゃなければ、アラビア数字を漢数字に変換する処理を行う
    if len(input_list) != 0:
        # 万、億、兆に対応するため、(桁数-1)÷4の商を代入する
        large_digits_length = (len(input_list) - 1) // 4
        # 一～千の位を変換するため、(桁数-1)÷4の余りを代入
        numbers_length = (len(input_list) - 1) % 4

        # large_digits_lengthが-1より大きい時、以下を繰り返す         
        while large_digits_length > -1:
            # large_digits_lengthが0のとき（inputが1～4桁の時）
            if large_digits_length == 0:
                # until_thousand_number2kanjiを呼び出し、漢数字に変換する
                output_str = until_thousand_number2kanji(numbers_length, output_str, reverse_list)
                large_digits_length -= 1
            
            # large_digits_lengthが0より大きい時（inputが5桁以上の時）
            elif large_digits_length > 0:
                # 入力された数値を下から4桁ずつ区切って、split_listに格納する
                split_list = []
                for i in range(4):
                    if 4 * large_digits_length + i < list_length:
                        split_list.append(reverse_list[4*large_digits_length + i])
                    else:
                        break

                # split_listが[0, 0, 0, 0]じゃないとき、漢数字に変換する
                if split_list.count(0) != 4:
                    output_str = until_thousand_number2kanji(len(split_list)-1, output_str, split_list) + large_digits_directory[10000 ** large_digits_length]
                large_digits_length -= 1
            # 無限ループ防止用
            else:
                large_digits_length -= 1
    
    # inputが0の時、そのまま「零」を返す
    else:
        output_str = numbers_directory[int_input]
    
    return output_str

# 漢数字をアラビア数字に変換する
@app.route("/v1/kanji2number/<input>", methods=["GET"])
def kanji2number(input):
    return "未実装です"

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
