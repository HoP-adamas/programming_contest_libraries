def Z_algo(S):
	L = len(S)
	lcp = [0]*L
	lcp[0] = L
	i = 1
	j = 0
	while i < L:
		while i + j < L and S[j] == S[i+j]: # 先頭からみて文字が一致しているかを見る
			j += 1
		if not j: # 先頭文字が違っていた場合
			i += 1
			continue
		lcp[i] = j # SとS[i:]との最長共通接頭辞の長さを記録
		k = 1
		while i + k < L and k + lcp[k] < j: # 探索した部分列内に収まっているものは結果を再利用する
			lcp[i+k] = lcp[k]
			k += 1
		# 上のループではみ出した際に次のiとjのループにつなげるための処理
		i += k
		j -= k
		
	return lcp