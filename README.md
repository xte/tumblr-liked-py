# tumblr-liked-py

python script to grab all the images from the posts you've liked on
tumblr.

## prerequisites

* python
* oauth2
* pytumblr <https://github.com/tumblr/pytumblr>
* gnu parallel

### debian/ubuntu

you can install pytumblr if you want, or just clone the repository and
create a symlink.

    sudo apt-get install python python-oauth2 git parallel
    git clone https://github.com/tumblr/pytumblr gh-pytumblr
    ln -s gh-pytumblr/pytumblr pytumblr

## how to use

0. register for developer API keys on tumblr <https://www.tumblr.com/oauth/apps> 
   and place the `consumer_key` and `consumer_secret` in 
   `credentials.json`.

1. run `python get_tokens.py` and follow the prompts to get your
   `oauth_token` and `oauth_token_secret` and put them in
   `credentials.json`.

2. run `python run.py`.
   this will print to STDOUT all the URLs of the images of posts you've
   liked. 
   i suggest redirecting it to a file or use `tee`:
   `python run.py | tee urls.txt`

3. use `wget` or `curl` with `parallel` to grab all the images:
   `cat urls.txt | egrep "^http" | parallel curl -q -O {}`.
