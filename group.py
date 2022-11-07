# Import external modules
import dateutil.parser as dateparser
from datetime import datetime, timedelta
# Import internal modules
from connect import get_graph
from config import FACEBOOK_GROUP_ID


def get_group_post_attachments(graph, since=None, until=None):
    """
    This function looks at the posts of a Facebook group from since to until.
    It returns a list of posts containing videos.

    :param graph: Graph as coming from get_graph function.
    :type graph: facebook.GraphAPI
    :param since: From when we are inspecting the group to find videos.
    :type since: str
    :param until: Up to when we want to inspect th group's post to find videos
    :type until: str
    :return:
    """
    # If since or until are None, set them to a default.
    if since is None:
        since = datetime.utcnow() - timedelta(days=1)
    if until is None:
        until = datetime.utcnow()
    video_list = []
    # Get all the posts
    posts = graph.get_connections(
        id=FACEBOOK_GROUP_ID,
        connection_name='feed',
        since=since,
        until=until,
        fields='attachments'
    )
    # Get 'data' because we are not interested in paging
    posts = posts['data']
    # Now loop through all of the posts and do some stuff
    for post in posts:
        try:
            attachments = post['attachments']['data']
            for attachment in attachments:
                # If it contains sub-attachments append them individually
                if 'subattachments' in attachment.keys():
                    subattachments = attachment['subattachments']['data']
                    for subattachment in subattachments:
                        if 'video' in subattachment['type']:
                            video_list.append(handle_videos(subattachment,
                                                            post, graph))
                else:
                    if 'video' in attachment['type']:
                        video_list.append(handle_videos(attachment, post,
                                                        graph))
        except KeyError:
            continue
    for video in video_list:
        pretty_print_video_alert(video)
    return video_list


def handle_videos(attachment, post, g):
    """
    This function handles what to do when an attachment is actually a video.
    In this case it just outputs the id of the attachment, the url to the video
    of the post, the thumbnail image, the id of the post, the message of the
    post (description) and the time at which it was created.

    :param attachment:
    :type attachment:
    :param post:
    :type post:
    :param g: graphAPI
    :type g: facebook.GraphAPI
    :return:video_id, url, image, post_id, post_message, time
    :rtype: tuple

    """
    # Get url, id and image of the video
    url = attachment['url']
    video_id = attachment['target']['id']
    image = attachment['media']['image']['src']
    # From the post get the time it was created at, message and id
    post_id = post['id']
    time = g.get_object(post_id)['created_time']
    post_message = g.get_object(post_id)['message']
    return video_id, url, image, post_id, post_message, time


def pretty_print_video_alert(video_tuple):
    """
    This function takes in a tuple coming from handle_videos function and does
    a pretty-print function to see some information about the videos found.
    :param video_tuple:
    :return:
    """
    print("Video upload date: {0}"
          .format(dateparser.parse(video_tuple[5])
                  .strftime("%H:%M:%S  %d-%m-%Y")))
    print("Video url: ", video_tuple[1])
    print("Video was attached to post with id: ", video_tuple[3])
    print("Post message was: ", video_tuple[4])
    print("-" * 80)


if __name__ == "__main__":
    gr, _ = get_graph()
    vid_list = get_group_post_attachments(gr, since='2018-01-01')
