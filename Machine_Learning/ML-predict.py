import os
import sys 
import random
#input abd file 
original_abd=str(sys.argv[1])
#biomarker number
n=str(sys.argv[2])
#此次数据前缀名
p=str(sys.argv[3])
os.system("mkdir "+p)

#生成十次随机数据集
for num in range(1,11):
    #abd file random
    #生成127个随机数
    ran_num=random.sample(range(1,600),127)
    #行号计数
    count_for_line_id=0
    #为每一行分配一个随机数
    ran_info={}
    with open(original_abd,"r") as fa:
        lines=fa.readlines()
    for i in lines[1:]:
        s=i.rstrip().split("\t")
        ran_info[ran_num[count_for_line_id]]=i
        count_for_line_id=count_for_line_id+1
    #给这些随机数排序
    sort_ran_num=sorted(ran_num)
    #写入文件
    abd=p+".ran"+str(num)+".txt"
    with open(abd,"w") as fw:
        fw.write(lines[0])
        for i in sort_ran_num:
            fw.write(ran_info[i])

    # abd文件切分成10分数据
    os.system("head -n 1 "+ abd + " >> title.txt")
    os.system("sed -n '2,13p' " + abd  + " >> 1.txt")
    os.system("sed -n '14,26p' " + abd  + " >> 2.txt")
    os.system("sed -n '27,38p' " + abd + " >> 3.txt")
    os.system("sed -n '39,51p' " + abd + " >> 4.txt")
    os.system("sed -n '52,63p' " + abd + " >> 5.txt")
    os.system("sed -n '64,76p' " + abd + " >> 6.txt")
    os.system("sed -n '77,89p' " + abd + " >> 7.txt")
    os.system("sed -n '90,102p' " + abd + " >> 8.txt")
    os.system("sed -n '103,115p' " + abd + " >> 9.txt")
    os.system("sed -n '116,128p' " + abd + " >> 10.txt")
    # 合并数据成相应的训练集 测试集
    os.system("cat title.txt 2.txt 3.txt 4.txt 5.txt 6.txt 7.txt 8.txt 9.txt 10.txt >> train1.txt")
    os.system("cat title.txt 1.txt 3.txt 4.txt 5.txt 6.txt 7.txt 8.txt 9.txt 10.txt >> train2.txt")
    os.system("cat title.txt 1.txt 2.txt 4.txt 5.txt 6.txt 7.txt 8.txt 9.txt 10.txt >> train3.txt")
    os.system("cat title.txt 1.txt 2.txt 3.txt 5.txt 6.txt 7.txt 8.txt 9.txt 10.txt >> train4.txt")
    os.system("cat title.txt 1.txt 2.txt 3.txt 4.txt 6.txt 7.txt 8.txt 9.txt 10.txt >> train5.txt")
    os.system("cat title.txt 1.txt 2.txt 3.txt 4.txt 5.txt 7.txt 8.txt 9.txt 10.txt >> train6.txt")
    os.system("cat title.txt 1.txt 2.txt 3.txt 4.txt 5.txt 6.txt 8.txt 9.txt 10.txt >> train7.txt")
    os.system("cat title.txt 1.txt 2.txt 3.txt 4.txt 5.txt 6.txt 7.txt 9.txt 10.txt >> train8.txt")
    os.system("cat title.txt 1.txt 2.txt 3.txt 4.txt 5.txt 6.txt 7.txt 8.txt 10.txt >> train9.txt")
    os.system("cat title.txt 1.txt 2.txt 3.txt 4.txt 5.txt 6.txt 7.txt 8.txt 9.txt >> train10.txt")

    os.system("cat title.txt 1.txt >> test1.txt")
    os.system("cat title.txt 2.txt >> test2.txt")
    os.system("cat title.txt 3.txt >> test3.txt")
    os.system("cat title.txt 4.txt >> test4.txt")
    os.system("cat title.txt 5.txt >> test5.txt")
    os.system("cat title.txt 6.txt >> test6.txt")
    os.system("cat title.txt 7.txt >> test7.txt")
    os.system("cat title.txt 8.txt >> test8.txt")
    os.system("cat title.txt 9.txt >> test9.txt")
    os.system("cat title.txt 10.txt >> test10.txt")
    #拆分数据集的meta信息和丰度信息
    for i in range(1,21):
        file_abd={}
        file_meta={}
        if (i<11):
            in_file="train"+str(i)+".txt"
        else:
            j=i-10
            in_file="test"+str(j)+".txt"
        with open(in_file,'r') as fr:
            lines=fr.readlines();
        for k in lines:
            s=k.rstrip().split('\t')
            file_abd[s[0]]=s[0]
            nn=int(n)
            for m in range(1,nn+1):
                file_abd[s[0]]=file_abd[s[0]]+"\t"+s[m]
            file_abd[s[0]]=file_abd[s[0]]+"\n"
            file_meta[s[0]]=s[0]+"\t"+s[nn+1]+"\n"
        
        input_abd_file=in_file.split(".txt")[0]+".abd"
        input_meta_file=in_file.split(".txt")[0]+".meta"

        with open(input_abd_file,"a") as fw:
            for s in file_abd:
                fw.write(file_abd[s])

        with open(input_meta_file,"a") as fw2:
            for s in file_meta:
                fw2.write(file_meta[s])
    str_num=str(num)
    #创建本次随机的文件夹，存入所有结果
    num_folder=p+"/"+str_num
    os.system("mkdir "+num_folder)
    #创建新文件夹，把本次随机abd的结果,以及10份train、test集存入备份
    bk_folder=num_folder+"/data-bk"
    os.system("mkdir "+bk_folder)
    os.system("mv *.txt "+bk_folder)
    #创建新文件夹，把abd meta结果存入备份
    dataset_folder=num_folder+"/dataset"
    os.system("mkdir "+dataset_folder)
    os.system("mv *.abd "+dataset_folder)
    os.system("mv *.meta "+dataset_folder)
    
    predict_file=num_folder+"/predict_true_rate.txt"
    valid_file=num_folder+"/validation.txt"
    with open(predict_file,"a")as fp:
        fp.write("fold"+"\t"+"XGBoost"+"\t"+"RF"+"\n")

    #10-fold XGBoost RF predict and validation
    for i in range(1,11):
        #predict
        XGB_folder=num_folder+"/XGB-top"+str(n)
        xgb_p="XGB-top"+str(n)+"."+str(i)+".txt"
        RF_folder=num_folder+"/RF-top"+str(n)
        rf_p="RF-top"+str(n)+"."+str(i)+".txt"
        
        os.system("Rscript /mnt/d/Bioinformatics/硒元素/正式实验/R/XGB_predict.R -t "+dataset_folder+"/train"+str(i)+".abd -i "+dataset_folder+"/test"+str(i)+".abd -m "+dataset_folder+"/train"+str(i)+".meta -o "+XGB_folder+" -p "+xgb_p)
        
        os.system("Rscript /mnt/d/Bioinformatics/硒元素/正式实验/R/RF_predict.R -t "+dataset_folder+"/train"+str(i)+".abd -i "+dataset_folder+"/test"+str(i)+".abd -m "+dataset_folder+"/train"+str(i)+".meta -o "+RF_folder+" -p "+rf_p)

        #validation
        xgb_out=XGB_folder+"/"+xgb_p
        rf_out=RF_folder+"/"+rf_p
        test_meta=dataset_folder+"/test"+str(i)+".meta"
        
        with open(xgb_out,"r") as fxg:
            xg=fxg.readlines();
        with open(rf_out,"r") as frf:
            rf=frf.readlines();
        with open(test_meta,"r") as ft:
            t=ft.readlines();
            
        with open(valid_file,"a")as fw:
            fw.write(str(i)+" fold validation data"+"\n")
            fw.write("sampleid"+"\t"+"XGB_predict"+"\t"+"RF_predict"+"\t"+"real_value"+"\n")
            count_one_fold=0
            count_xgb=0
            count_rf=0
            for j in xg:
                for k in rf:
                    for m in t[1:]:
                        sxg=j.rstrip().split('\t')
                        srf=k.rstrip().split('\t')
                        st=m.rstrip().split('\t')
                        #sampleid equal
                        if(sxg[0]==srf[0]==st[0]):
                            count_one_fold=count_one_fold+1
                            #xgboost=real
                            if(sxg[1]==st[1]):
                                count_xgb=count_xgb+1
                            #rf=real
                            if(srf[1]==st[1]):
                                count_rf=count_rf+1
                            fw.write(sxg[0]+"\t"+sxg[1]+"\t"+srf[1]+"\t"+st[1]+"\n")
            xgb_true_rate=count_xgb/count_one_fold
            rf_true_rate=count_rf/count_one_fold
            with open(predict_file,"a")as fp:
                fp.write(str(i)+"\t")
                fp.write(str(xgb_true_rate)+"\t")
                fp.write(str(rf_true_rate)+"\n")
    #10-fold done, caculate for average predict_true_rate
    xgp=0
    rfp=0
    with open(predict_file,"r") as fp:
        lines=fp.readlines();
    for i in lines[1:]:
        s=i.rstrip().split('\t')
        xgp=xgp+float(s[1])
        rfp=rfp+float(s[2])
    xgp_avg=xgp/10
    rfp_avg=rfp/10
    with open(predict_file,"a")as fp:
        fp.write(str_num+"times_average"+"\t"+str(xgp_avg)+"\t"+str(rfp_avg)+"\n")

    os.system("mv "+ bk_folder+ "/"+original_abd +" "+original_abd)

# 10 random abd file done, caculate average predict_true_rate for 10(abd)*10(fold)

os.system("head -n 1 "+ p+"/1/predict_true_rate.txt" + " >> "+p+"/title.txt")
cat_str="cat "+p+"/title.txt"

for l in range(1,11):
    i=str(l)
    os.system("sed -n '12p' "+p+"/"+i+"/predict_true_rate.txt >> "+p+"/"+i+".txt")
    cat_str=cat_str+" "+p+"/"+i+".txt"

os.system(cat_str+">> "+p+"/all_predict_rate")
os.system("rm -rf "+p+"/*.txt") 
#重命名
os.system("mv "+p+"/all_predict_rate "+p+"/all_predict_rate.txt")
xgp=0
rfp=0
all_p=p+"/all_predict_rate.txt"
with open(all_p,"r") as fp:
    lines=fp.readlines();
for i in lines[1:]:
    s=i.rstrip().split('\t')
    xgp=xgp+float(s[1])
    rfp=rfp+float(s[2])
xgp_avg=xgp/10
rfp_avg=rfp/10
with open(all_p,"a")as fp:
    fp.write("all_average"+"\t"+str(xgp_avg)+"\t"+str(rfp_avg)+"\n")
    
os.system("mv "+original_abd +" "+p+"/"+original_abd)