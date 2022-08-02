## Music Player
Music Player is an educational application to further my understanding of Python 3 and Redis. This application consists of the following
components / functionality:  

    * Easy-to-use GUI through **Tkinter**  
    * Encrypted User Authentication  
    * Loading Featured Playlists through **Spotipy**  
    * Music Playback  
    * Track Favorites  

Redis allows this application to manage user accounts and user favorites through key-pair values. Unique keys, similar to a primary key
or unique identifier that you might come across in SQL are used to facilitate this functionality. Additionally, the value that is stored  
next to each key is a JSON-formatted string. Objects are serialized within the application as needed, passed to the Redis database, and
that same string is deserialized into a compact object form when needed by the application. Explicit examples of this idea are provided
below:

    ** User Account Key **

    ```
    user:<email>

    ```

    ** Favorited Track Key **

    ```
    favorite:<track_id>:<email>
    ```

## Requirements

In order to run this application you will need to undergo several steps. Initially, you will need to setup a virtual environment. If you are
unfamiliar with this process, a quick walkthrough is provided below.

First, you will need to clone the directory.

    ```
    git clone https://github.com/guyr18/music-player.git
    ```

Next, navigate to this directory on your local machine.

    ```
    cd music-player
    ```

Python 3.10 is recommended for running this application. I will be assuming that you have it installed for the remainder of this text. You may
create a virtual environment through the following command:

    ```
    python3.10 -m virtualenv env
    ```

We have now created a virtual environment with the name **env**. To confirm this, simply list the files in the directory and check that a directory  
named **env** exists (**ls** command). Next, we want to activate it, which can be done as follows:

    ```
    source env/bin/activate
    ```

For future reference, this virtual environment may be deactivated with the **deactivate** command. You will now want to install the list of required
dependencies that are found in **requirements.txt**. To do so, run the following command in your virtual environment terminal:

    ```
    pip install -r requirements.txt
    ```

Following this, you will need to ensure that your Redis server is running properly. I will not cover that in this tutorial but a great reference is the
following: https://redis.io/docs/getting-started/  

The settings that this application uses are defined in **conf.txt**. You will need to update this file to ensure that the application can setup a client
object on your Redis server instance. It follows the 3-line format listed below:

    ```
    <host_name>
    <port_number>
    <password>
    ```

If your password is the empty string, you will need to make their is an empty third line in **conf.txt**. Deleting it will result in an error.

When your server is up and running, you will also need a preliminary account stored in the Redis datastore to access this application. I have provided a **setup.py** file that you will need to run in order to create that account.

    ```
    python3.10 setup.py
    ```

You should now be ready to run the application. Below is a sample video demonstrating the intended use of the functionality:
