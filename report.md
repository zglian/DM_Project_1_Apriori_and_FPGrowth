# Data Mining Project1

F74102030 資訊114 練智剛

---

## 1.1 What do you observe in the below 4 scenarios? What could be the reason?

- a. low support, low confidence
條件最為寬鬆的情況，因為support的值比較低，frequent itemsets較多，在confidence也低的情況下，彼此之間較低的關聯性也能夠形成association rule，是四種裡面能夠產生最多組別的情況
- b. low support, high confidence
因為support的值比較低，frequent itemsets較多，在confidence也高的情況下，彼此之間需要較高的關聯性才能夠形成association rule，相較於第一種情況所產生的組別會比較少，此種情況下最具有參考價值
- c. high support, low confidence
因為support的值比較高，frequent itemsets較少，儘管confidence低，但是因為原本的frequent itemsets就很少，所以僅有較少數的組別能夠形成association rule，相較於第一種情況所產生的組別也會比較少
- d. high support, high confidence
條件最為嚴格，因為support的值比較高，frequent itemsets較少，而confidence也很高，彼此之間需要較高的關聯性才能夠形成association rule，所以產生的組別最少

## 1.2 Runtime statistics

Apriori
min_sup = 0.05, min_conf = 0.05 --> 77.45 seconds
min_sup = 0.05, min_conf = 0.2 --> 76.84 seconds
min_sup = 0.2, min_conf = 0.05 --> 1.35 seconds
min_sup = 0.2, min_conf = 0.2 --> 1.26 seconds

FPgrowth
min_sup = 0.05, min_conf = 0.05 --> 80.58 seconds
min_sup = 0.05, min_conf = 0.2 --> 79.98 seconds
min_sup = 0.2, min_conf = 0.05 --> 1.13 seconds
min_sup = 0.2, min_conf = 0.2 --> 1.02 seconds

explanation:
a. 在low min_sup和low min_conf的情況下，因為可以通過的frequent itemset較多，每次的運算量較大，所以執行時間也相對較多

b. 在low min_sup和high min_conf的情況下，運行時間略少於上一組a，因為我的演算法設計是，最c 後要輸出結果前才過濾掉confidence不夠高的組別，所以兩組的計算量是差不多的，運行時間相差不大

c. 在high min_sup 和low min_conf的情況下，可以通過的frequent itemsets少，所以每個階段的運算量較低，總運行時間短

d. 在high min_sup 和high min_conf的情況下，運行時間略少於上一組c，同理於a和b組，兩者的運算量差不多，只差在最後過濾confidence的階段，所以兩組的計算量是差不多的，運行時間相差不大

## 1.3 Any topics you are interested in

我觀察了不同tlen下所需要的執行時間，以及所產生的assiciation rule。

參數設定:
min_sup=0.05, min_conf=0.05
指令 ./gen lit -ntrans 3 -tlen {from 5 to 12} -conf 0.3 -nitems 0.05

ten=5 running time=0.63s -->77組
ten=6 running time=0.94s -->149組
ten=7 running time=1.54s -->285組
ten=8 running time=2.53s -->631組
ten=9 running time=4.47s -->1317組
ten=10 running time=7.54s -->2863組
ten=11 running time=12.3s -->5985組
ten=12 running time=21.9s -->11979組

從上述的統計資料中可以觀察出來，當tlen越長，所需要的running time也越長，因為每個客戶購買的item數量增加，每個物品出現的support越高，所以可以通過min_sup的機會也越大，造成運算量的增加，而產生的association rule，大致上是每增加一，所產生的association rules 會變成原本的兩倍

### Bonus

我在kaggle上找了一個groceries的銷售紀錄，裡面紀錄了不同members每次的購買紀錄，有將近39000筆資料，總共有3899為members，以及168項商品，我試圖用這些資料找出每一位members所買的物品之間的關聯性，我嘗試了不同min_sup和min_conf的輸入，以下是一些紀錄:

a. min_sup=0.05, min_conf=0.05 -->260組
low sup,  low confidence

b. min_sup=0.05, min_conf=0.1 -->250組
low sup,  提高confidence

c. min_sup=0.05, min_conf=0.2 -->155組
low sup,  high confidence

d. min_sup=0.05, min_conf=0.5 -->12組
low sup,  high confidence

d. min_sup=0.05, min_conf=0.7 -->0組
low sup,  high confidence

e. min_sup=0.1, min_conf=0.05 -->27組
low sup,  low confidence

f. min_sup=0.2, min_conf=0.05 -->0組
high sup,  low confidence

g. min_sup = 0.2, min_conf=0.2 -->0組
high sup,  high sup

從這些不同參數組別可以看出來，當support稍微提高，frequent itemsets的數量就會大幅下降，這可能來自於商品數量過於多，每位會員買的東西過於分散，所以要超過min_sup並不容易。而當confidence稍微提高，所產生的association rule 減少速度比較慢，可能是顧客都固定買幾樣相同的東西，所以confidence比較高。我觀察了整理過後的資料後，發現很多會員都買同一到兩樣物品，會員的消費習慣較為單一。上述兩點造成只能在low sup, low confidence的情形下找到較多的association rules。其中比較有趣的是第d組這個情況，在sup低、conf相對高的情況下，除了一組以外的assocation rules，其他的consequence都只有milk這個商品，可能的推斷是，此間grocery的牛奶價格低，大家買東西都會順便帶一瓶走，或者是當地的飲食習慣常喝牛奶，所以每次來都會買一瓶走。