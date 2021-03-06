import numpy as np
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from collections import Counter
from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt 
from tkinter import *
from tkinter import messagebox
root = Tk()
# root.geometry("900x300")
root.title("Rating Generator from Product Reviews")

def readwords(filename):
    f = open(filename)
    words = [line.rstrip() for line in f.readlines()]
    return words

positive = readwords('positive-words.txt')
negative = readwords('negative-words.txt')
stopwords = set(STOPWORDS) 

dataset = pd.read_csv('dataMeizu.csv', delimiter=',')           #######################
array = []
corpus = []
polarity = []
stars, top_positive, top_negative = [], [], []
positive_words = []
negative_words = []
zeros, max_pos, max_neg = 0, 0, 0
zeros = 0
ones = 0
sum_of_stars, flag = 0, 0

no_of_reviews = len(dataset)-1     

for i in range(0,no_of_reviews):
    review = re.sub('[^a-zA-Z]',' ',str(dataset['review_text'][i]))
    star = re.sub('0-9',' ',dataset['review_star'][i])
    review = review.lower()
    review = review.split()
    star = star.split()
    star = float(star[0])
    #ps = PorterStemmer()
    #review = [ps.stem(word) for word in review
    #               if not word in set(stopwords.words('english'))]
    review = ' '.join(review) 
    count = Counter(review.split())
    pos = 0
    neg = 0
    for key, val in count.items():
        key = key.rstrip('.,?!\n') # removing possible punctuation signs
        if(('not' in key) or ('no' in key)):
            flag = 1
            # print(key)
            continue
        if(flag == 1):
            # print(key)
            if(key in positive):
                neg += val
                # print(neg)
            if(key in negative):
                pos += val
                # print(pos)
            flag = 0
            continue
        if key in positive:
            pos += val
            positive_words.append(key)
        if key in negative:
            neg += val
            negative_words.append(key)

    if(pos > max_pos):
        max_pos = pos
        # print(review,pos,neg)
        top_positive.append(review)
    if(neg > max_neg):
        max_neg = neg
        top_negative.append(review)
        # print(review,pos,neg)

    if(pos >= neg):
        label = 1
        ones +=1
    else:
        label = 0
        zeros += 1
    sum_of_stars += star
    stars.append(star)
    polarity.append(label)
    corpus.append(review)
#print(corpus)
#print(polarity)
#print(stars)
#print(positive_words)
#print(negative_words)
#print(array)

print("\n")

avg = sum_of_stars/no_of_reviews
rating = ((ones - zeros)/(ones + zeros))*5

def generate_positive_wc():
    unique_string1=(" ").join(positive_words)
    wordcloud = WordCloud(width = 800, height = 800, 
                    background_color ='white', 
                    stopwords = stopwords, 
                    min_font_size = 10).generate(unique_string1) 

    plt.figure(figsize = (8, 8), facecolor = None) 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 

    plt.show() 

def generate_negative_wc():
    unique_string2=(" ").join(negative_words)
    wordcloud = WordCloud(width = 800, height = 800, 
                    background_color ='white', 
                    stopwords = stopwords, 
                    min_font_size = 10).generate(unique_string2) 

    plt.figure(figsize = (8, 8), facecolor = None) 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 

    plt.show()


cwgt=Canvas(root, width=665,height=600)
cwgt.pack(expand=True,fill=BOTH)
image1=PhotoImage(file="summer_tech_pattern2.png")
# keep a link to the image to stop the image being garbage collected
cwgt.img=image1
cwgt.create_image(0,0,anchor=NW, image=image1)

l1 = Label(cwgt, text = "Positive reviews = ",font=("Arial Bold", 15),fg='#000099')
cwgt.create_window(20,20,anchor=NW, window=l1)
v1 = IntVar()
l11 = Label(cwgt, textvariable = v1,font=("Arial Bold", 10))
v1.set(ones)
cwgt.create_window(350,20,anchor=NW, window=l11)

l2 = Label(cwgt, text = "Negative reviews = ",font=("Arial Bold", 15),fg='#000099')
cwgt.create_window(20,60,anchor=NW, window=l2)
v2 = IntVar()
l22 = Label(cwgt, textvariable = v2,font=("Arial Bold", 10))
v2.set(zeros)
cwgt.create_window(350,60,anchor=NW, window=l22)

l3 = Label(cwgt, text = "Calculated Rating = ",font=("Arial Bold", 15),fg='#000099')
cwgt.create_window(20,100,anchor=NW, window=l3)
v3 = IntVar()
l33 = Label(cwgt, textvariable = v3,font=("Arial Bold", 10),fg='#FF0000')
v3.set(round(rating, 3))
cwgt.create_window(350,100, anchor=NW,window=l33)

l4 = Label(cwgt, text = "Average Actual Rating = ",font=("Arial Bold", 15),fg='#000099')
cwgt.create_window(20,140,anchor=NW, window=l4)
v4 = IntVar()
l44 = Label(cwgt, textvariable = v4,font=("Arial Bold", 10))
v4.set(round(avg, 3))
cwgt.create_window(350,140,anchor=NW, window=l44)

l5 = Label(cwgt, text = "Top Positive Review = ",font=("Arial Bold", 15),fg='#000099')
cwgt.create_window(20,180,anchor=NW, window=l5)
l6 = Label(cwgt, text = "Top Negative Review = ",font=("Arial Bold", 15),fg='#000099')
cwgt.create_window(350,180,anchor=NW, window=l6)

v5 = StringVar()
l55 = Label(cwgt, textvariable = v5,justify=LEFT,wraplength=300,font=("Arial Bold", 10))
cwgt.create_window(20,220,anchor=NW, window=l55)
v5.set(top_positive[len(top_positive)-1])


v6 = StringVar()
l66 = Label(cwgt, textvariable = v6,justify=LEFT,wraplength=300,font=("Arial Bold", 10))
cwgt.create_window(350,220,anchor=NW, window=l66)
v6.set(top_negative[len(top_negative)-1])

b1 = Button(cwgt, text ="Generate Positive WC", command = generate_positive_wc,font=("Arial Bold", 10),bg='#31C12F') 
cwgt.create_window(150,550, anchor=NW,window=b1)
b2 = Button(cwgt, text ="Generate Negative WC", command = generate_negative_wc,font=("Arial Bold", 10),bg='#31C12F') 
cwgt.create_window(340,550, anchor=NW,window=b2)

# b1=Button(cwgt, text="Hello", bd=0)
# cwgt.create_window(40,40, window=b1)


# l1 = Label(f, text = "Positive reviews = ",font=("Arial Bold", 15),fg='#000099')
# l1.grid(row=0, column=0)
# v1 = IntVar()
# l11 = Label(f, textvariable = v1,font=("Arial Bold", 10))
# l11.grid(row=0, column=1)
# v1.set(ones)

# l2 = Label(f, text = "Negative reviews = ",font=("Arial Bold", 15),fg='#000099')
# l2.grid(row=1, column=0)
# v2 = IntVar()
# l22 = Label(f, textvariable = v2,font=("Arial Bold", 10))
# l22.grid(row=1, column=1)
# v2.set(zeros)

# l3 = Label(f, text = "Calculated Rating = ",font=("Arial Bold", 15),fg='#000099')
# l3.grid(row=2, column=0)
# v3 = DoubleVar()
# l33 = Label(f, textvariable = v3,font=("Arial Bold", 10))
# l33.grid(row=2, column=1)
# v3.set(round(rating, 3))

# l4 = Label(f,  text = "Average Actual Rating = ",font=("Arial Bold", 15),fg='#000099')
# l4.grid(row=3, column=0)
# v4 = DoubleVar()
# l44 = Label(f,  textvariable = v4,font=("Arial Bold", 10))
# l44.grid(row=3, column=1)
# v4.set(round(avg, 3))

# l5 = Label(f, text = "Top Positive Review = ",font=("Arial Bold", 15),fg='#000099')
# l5.grid(row=4, column=0)
# v5 = StringVar()
# l55 = Label(f, textvariable = v5,justify=LEFT,wraplength=300,font=("Arial Bold", 10))
# l55.grid(row=4, column=1,rowspan=2,columnspan=4)
# v5.set(top_positive[len(top_positive)-1])

# l6 = Label(f, text = "Top Negative Review = ",font=("Arial Bold", 15),fg='#000099')
# l6.grid(row=6, column=0)
# v6 = StringVar()
# l66 = Label(f, textvariable = v6,justify=LEFT,wraplength=300,font=("Arial Bold", 10))
# l66.grid(row=6, column=1,rowspan=2,columnspan=4)
# v6.set(top_negative[len(top_negative)-1])

# b1 = Button(f, text ="Generate Positive WC", command = generate_positive_wc,font=("Arial Bold", 10),bg='#C0C0C0') 
# b1.grid(row=8, column=0)
# b2 = Button(f, text ="Generate Negative WC", command = generate_negative_wc,font=("Arial Bold", 10),bg='#C0C0C0') 
# b2.grid(row=8, column=2)

#root.geometry('220x200+250+250')

root.mainloop()
# print('Positive reviews = ', ones)
# print('Negative reviews = ', zeros)
# print('Calculated Rating = ', rating)
# print('Average Actual Rating = ', avg)
# print("\n")
# print(top_positive[len(top_positive)-1],"\n")
# print(top_negative[len(top_negative)-1])

# unique_string1=(" ").join(positive_words)
# wordcloud = WordCloud(width = 800, height = 800, 
# 				background_color ='white', 
# 				stopwords = stopwords, 
# 				min_font_size = 10).generate(unique_string1) 

# plt.figure(figsize = (8, 8), facecolor = None) 
# plt.imshow(wordcloud) 
# plt.axis("off") 
# plt.tight_layout(pad = 0) 

# plt.show() 

# unique_string2=(" ").join(negative_words)
# wordcloud = WordCloud(width = 800, height = 800, 
# 				background_color ='white', 
# 				stopwords = stopwords, 
# 				min_font_size = 10).generate(unique_string2) 

# plt.figure(figsize = (8, 8), facecolor = None) 
# plt.imshow(wordcloud) 
# plt.axis("off") 
# plt.tight_layout(pad = 0) 

# plt.show() 

