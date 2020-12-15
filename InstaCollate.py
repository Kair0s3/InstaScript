# 2 different Instagram-Python Modules found that I can reference
# Try 1 - Instaloader
# Using an Instagram Instance to enumerate #tags
# Next if doesnt work - InstaPy ^TOBEREMOVED
# Credits to Instaloader by Alexander Graf (https://github.com/aandergr)
import instaloader as ig
from datetime import datetime
import os
import wget


now = datetime.now()
runtime = now.strftime("%m-%d-%Y_%H-%M-%S")
output = os.path.dirname(os.path.abspath(__file__)) + f"/Download@{runtime}/"
L = ig.Instaloader()

# Modify to max post/images you want to download related to the hashtag
max = 3

# Modify the script mode below
# Mode 0 - Basically downloads everything based off Instaloader (I feel this might take up a lot of space and download stuff I dont really want)
# Mode 1 - Images/Videos Only
# IMPROVEMENT IN FUTURE
# Mode 1 Addition - JSON file containing the file paths of the downloaded files and by whom
# Mode 2 - Post's Images/Videos, captions and and JSON file containing the file paths of the downloaded files and by whom
mode = 1

# Ask for user input on hashtag to find
search = 'tag'
hashtag = ig.Hashtag.from_name(L.context, search)

counter = 0 #tobechangedback
for post in hashtag.get_top_posts(): # change to get_top_posts() if you want to most trending post or get_posts() for recent
    # post is an instance of instaloader.Post
    if (counter < max):
        if (mode == 0):
            L.download_post(post, target=f"#{search}-{post.profile}")
        elif (mode == 1 or 2):
            if not os.path.isdir(output):
                os.mkdir(output)
            if (post.typename == "GraphSidecar"):
                newFolder = f'{output}{post.profile}/'
                # print (newFolder)
                # print (post.tagged_users)
                # sample output - ['person1', 'person2']
                print (post.url)
                # make new directory to store the sidecar image/videos
                if not os.path.isdir(newFolder):
                    os.mkdir(newFolder)
                sidecar = post.get_sidecar_nodes()
                # Get the sidecar nodes
                slide = 1
                for side in sidecar:
                    # Check if video/image - then get respective file
                    if side.is_video:
                        #print (side.video_url)
                        wget.download(side.video_url, f'{newFolder}{str(post.date_local).replace(":", "-").strip(" ")}_{slide}.mp4')
                    else:
                        #print (side.display_url)
                        wget.download(side.display_url, f'{newFolder}{str(post.date_local).replace(":", "-").strip(" ")}_{slide}.jpg')
                    slide += 1
            elif (post.typename == "GraphVideo"):
                tagged = post.tagged_users
                # if (tagged):
                #     print (tagged)
                videoUrl = post.video_url
                wget.download(videoUrl, f'{output}{str(post.date_local).replace(":", "-").strip(" ")}.mp4')
            elif (post.typename == "GraphImage"):
                tagged = post.tagged_users
                # if (tagged):
                #     print (tagged)
                imageUrl = post.url
                print (post.url)
                wget.download(imageUrl, f'{output}{str(post.date_local).replace(":", "-").strip(" ")}.jpg')
        #elif (mode == 3):
        print (post.profile + " - " + post.typename)
        counter += 1
    else:
        break
 # I can probably implement json to store some information eg. captions
