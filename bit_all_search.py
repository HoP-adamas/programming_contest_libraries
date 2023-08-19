for i in range(1<<n):
	L = []  # 問題にあったリスト
	for j in range(n):  # このループが一番のポイント
		if ((i >> j) & 1):  # 順に右にシフトさせ最下位bitのチェックを行う
			'''something'''  # フラグが立っていたら何かしらの操作をする。
