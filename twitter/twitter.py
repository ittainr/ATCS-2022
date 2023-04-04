from models import *
from database import init_db, db_session
from datetime import datetime

class Twitter:
    #The current user
    log=None

    """
    The menu to print once a user has logged in
    """
    def print_menu(self):
        print("\nPlease select a menu option:")
        print("1. View Feed")
        print("2. View My Tweets")
        print("3. Search by Tag")
        print("4. Search by User")
        print("5. Tweet")
        print("6. Follow")
        print("7. Unfollow")
        print("0. Logout")
    
    """
    Prints the provided list of tweets.
    """
    def print_tweets(self, tweets):
        for tweet in tweets:
            print("==============================")
            print(tweet)
        print("==============================")

    """
    Should be run at the end of the program
    """
    def end(self):
        print("Thanks for visiting!")
        db_session.remove()
    
    """
    Registers a new user. The user
    is guaranteed to be logged in after this function.
    """
    def register_user(self):
        while True:
            fail=False
            username=input("What will your twitter handle be?\n")
            password=input("Enter a password\n")
            check=input("Re-enter your password\n")
            for name in db_session.query(User.username):
                if username==name[0]:
                    print("That username is already taken. Try again.\n")
                    fail=True
                    break
            if fail:
                continue
            if password!=check:
                print("Those passwords don't match. Try again.\n")
            else:
                user=User(username=username, password=password)
                db_session.add(user)
                print(f"\nWelcome {username}!")
                db_session.commit()
                return user

    """
    Logs the user in. The user
    is guaranteed to be logged in after this function.
    """
    def login(self):
        while True:
            username=input("Username: ")
            password=input("Password: ")
            for user in db_session.query(User).all():
                if user.username==username and user.password==password:
                    print(f"Welcome {username}!")
                    return user
            print("Invalid username or password.")

    
    def logout(self):
        self.end()
        quit()

    """
    Allows the user to login,  
    register, or exit.
    """
    def startup(self):
        choice=int(input("Please select a menu option:\n1. Login\n2. Register\n0. Exit\n"))
        if choice==1:
            return self.login()
        elif choice==2:
            return self.register_user()
        else:
            self.logout()

    def follow(self):
        follow=input("Enter the username of the user you want to follow:\n")
        user=db_session.query(User).where(User.username==follow).first()
        for name in db_session.query(Follower.following_id).where(Follower.follower_id==self.log.username).all():
            if user.username == name[0]:
                print(f"You already follow {user}")
                return
        db_session.add(Follower(follower_id=self.log.username, following_id=user.username))
        db_session.commit()
        print(f"You now follow {user}")

    def unfollow(self):
        unfollow=input("Enter the username of the user you want to unfollow:\n")
        user=db_session.query(User).where(User.username==unfollow).first()
        for follower in db_session.query(Follower).where(Follower.follower_id==self.log.username).all():
            if user.username == follower.following_id:
                db_session.delete(follower)
                db_session.commit()
                print(f"You no longer follow {user}")
                return
        print(f"You don't follow {user}")

    def tweet(self):
        content = input("Enter the message you want to tweet: ")
        tags = input("Enter tags (seperate by spaces): ")
        timestamp = datetime.now()
        new_tweet = Tweet(content=content, timestamp=timestamp, username=self.log.username)
        tag = db_session.query(Tag).all()
        for t in tags.split():
            j=True
            for a in tag:
                if t==a.content:
                    new_tweet.tags.append(a)
                    j=False
                    break
            if j:
                g = Tag(content=t)
                new_tweet.tags.append(g)
        db_session.add(new_tweet)
        db_session.commit()
    
    def view_my_tweets(self):
        self.print_tweets(db_session.query(Tweet).where(Tweet.username==self.log.username))
    
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
        users = []
        following = db_session.query(User).where(Follower.follower_id == self.log.username)
        for i in following:
            users.append(i.username)
        tweet = db_session.query(Tweet).filter(Tweet.username.in_(users)).order_by(Tweet.timestamp.desc()).limit(5).all()
        self.print_tweets(tweet)

    def search_by_user(self):
        entered_user = input("Enter a user: \n")
        users = db_session.query(User).filter_by(username = entered_user)
        if users.count == 0:
            print("No tweets by this user")
        else:
            tweets = users[0].tweets
            if len(tweets) == 0:
                print("No tweets by this user")
            else:
                self.print_tweets(tweets)

    def search_by_tag(self):
        entered_tag = input("Enter a tag: \n")
        tags = db_session.query(Tag).filter_by(content = entered_tag)
        if tags.count == 0:
            print("No tweets with this tag")
        else:
            tweets = tags[0].tweets
            if len(tweets) == 0:
                print("No tweets with this tag")
            else:
                self.print_tweets(tweets)

    """
    Allows the user to select from the 
    ATCS Twitter Menu
    """
    def run(self):
        init_db()

        print("Welcome to ATCS Twitter!")
        self.log=self.startup()

        while True:
            self.print_menu()
            option = int(input(""))

            if option == 1:
                self.view_feed()
            elif option == 2:
                self.view_my_tweets()
            elif option == 3:
                self.search_by_tag()
            elif option == 4:
                self.search_by_user()
            elif option == 5:
                self.tweet()
            elif option == 6:
                self.follow()
            elif option == 7:
                self.unfollow()
            else:
                self.logout()
