import os
import re
import time
import requests
import pdf_generator
from pytube import YouTube
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi


class YouTubeTranscription:

    def __init__(self):
        pass

    def get_video_id(self, url):
        """Extract the video ID from a YouTube URL."""
        parsed_url = urlparse(url)
        if parsed_url.hostname == 'youtu.be':
            return parsed_url.path[1:]
        if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
            if parsed_url.path == '/watch':
                return parse_qs(parsed_url.query)['v'][0]
            if '/shorts/' in parsed_url.path:
                return parsed_url.path.split('/shorts/')[1]
        return None

    def get_transcript(self, url):
        """Get the transcript of a YouTube video."""
        video_id = self.get_video_id(url)
        if not video_id:
            print("Invalid YouTube URL")
            return ""
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            final_transcript = ' '.join([entry['text'] for entry in transcript])
            return final_transcript
        except Exception as e:
            try:
                pattern = r'\((MANUALLY CREATED)\)\s+-\s+(\w+-\w+)\s+\("(.+)"\)'
                matches = re.search(pattern, str(e))

                if matches:
                    language_code = matches.group(2)
                    transcript = YouTubeTranscriptApi.get_transcript(video_id=video_id, languages=[language_code])
                    final_transcript = ' '.join([entry['text'] for entry in transcript])
                    return final_transcript
                else:
                    print("Language code not found.")
                    print(f"An error occurred: {str(e)}")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
            return ""

    @staticmethod
    def extract_url_from_text(text):
        """Extract URL from text using regex."""
        url_pattern = r'https?://(?:www\.)?(?:youtube\.com|youtu\.be)/\S+'
        match = re.search(url_pattern, text)
        return match.group(0) if match else None

    def get_video_info(self, url):
        """Get important video information.

        Components are:
            - title
            - description
            - thumbnail url,
            - publish_date
            - channel_author
            - and more.
        """

        yt = YouTube(url)
        video_info = {}

        try:
            video_info["title"] = yt.title
        except Exception as e:
            video_info["title"] = "Unknown"
            print(f"Error retrieving title: {e}")

        try:
            video_info["view_count"] = yt.views
        except Exception as e:
            video_info["view_count"] = 0
            print(f"Error retrieving view count: {e}")

        try:
            video_info["length"] = yt.length
        except Exception as e:
            video_info["length"] = 0
            print(f"Error retrieving length: {e}")

        try:
            video_info["author"] = yt.author
        except Exception as e:
            video_info["author"] = "Unknown"
            print(f"Error retrieving author: {e}")

        return video_info

    def get_video_info2(self, url):

        video_id = self.get_video_id(url)

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        }

        json_data = {
            'context': {
                'client': {
                    'hl': 'en',
                    'gl': 'US',
                    'remoteHost': '2001:19f0:1000:289d:5400:5ff:fe02:6648',
                    'deviceMake': '',
                    'deviceModel': '',
                    'visitorData': 'Cgt0WFg1bEI5Tndmdyjfo760BjIKCgJVUxIEGgAgGA%3D%3D',
                    'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36,gzip(gfe)',
                    'clientName': 'WEB',
                    'clientVersion': '2.20240710.01.00',
                    'osName': 'Windows',
                    'osVersion': '10.0',
                    'originalUrl': 'https://www.youtube.com/watch?v=hpIOx2eGQS4&pp=ygUJbGFuZ2NoYWlu',
                    'screenPixelDensity': 2,
                    'platform': 'DESKTOP',
                    'clientFormFactor': 'UNKNOWN_FORM_FACTOR',
                    'configInfo': {
                        'appInstallData': 'CN-jvrQGEM3XsAUQ0PqwBRCJ6K4FEIvPsAUQ1o-xBRDEjLEFEJ2msAUQoJSxBRDX6a8FEJCSsQUQ97H_EhDPqLAFENPhrwUQ0I2wBRCO2rAFENjdsAUQt6uwBRCnk7EFEMnXsAUQ3Y6xBRDr6P4SEMr5sAUQ65OuBRClwv4SENv-tyIQl4OxBRDZya8FEOrDrwUQ1KGvBRCIh7AFEPSrsAUQqtiwBRCI468FEPrwsAUQlpWwBRDW3bAFEKWWsQUQ_IWwBRClk7EFEMnmsAUQsdywBRDbr68FEP-KsQUQ5fSwBRDj0bAFEMzfrgUQvYqwBRDJ968FELax_xIQ6YmxBRD-6rAFEI_EsAUQlP6wBRCj7bAFEJWVsQUQ7qKvBRDh7LAFEKiasAUQsO6wBRDvzbAFENiEsQUQlImxBRD2q7AFEL2ZsAUQgqL_EhCT77AFENaLsQUQk_yvBRC3srAFEJ3QsAUQ4tSuBRDf9bAFEIO5_xIQ1YiwBRDwjrEFEMSSsQUQvbauBRCa8K8FEIC7_xIQ3ej-EhCmmrAFEO6IsQUQooGwBRCNzLAFEKP4sAUQuJOxBRC3768FELfq_hIQjan_EhCYu_8SEJPxsAUQ08OwBSokQ0FNU0ZSVVdwYjJ3RE56a0JvT3o5QXZvc1FUMjdRWWRCdz09',
                    },
                    'screenDensityFloat': 1.5,
                    'userInterfaceTheme': 'USER_INTERFACE_THEME_LIGHT',
                    'timeZone': 'UTC',
                    'browserName': 'Chrome',
                    'browserVersion': '126.0.0.0',
                    'acceptHeader': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'deviceExperimentId': 'ChxOek01TURJNE5Ua3dNakl6TkRrd016VTFOdz09EN-jvrQGGN-jvrQG',
                    'screenWidthPoints': 458,
                    'screenHeightPoints': 593,
                    'utcOffsetMinutes': 0,
                    'memoryTotalKbytes': '8000000',
                    'clientScreen': 'WATCH',
                    'mainAppWebInfo': {
                        'graftUrl': '/watch?v=hpIOx2eGQS4&pp=ygUJbGFuZ2NoYWlu',
                        'pwaInstallabilityStatus': 'PWA_INSTALLABILITY_STATUS_CAN_BE_INSTALLED',
                        'webDisplayMode': 'WEB_DISPLAY_MODE_BROWSER',
                        'isWebNativeShareAvailable': True,
                    },
                }
            },
            'videoId': str(video_id),
        }

        response = requests.post('https://www.youtube.com/youtubei/v1/next',
                                 headers=headers, json=json_data)

        all_data = response.json()

        try:
            data = all_data['contents']['twoColumnWatchNextResults']['results']['results']['contents']

            req_data = {}
            try:
                req_data['subscription'] = data[1]['videoSecondaryInfoRenderer']['owner']['videoOwnerRenderer']['subscriberCountText']['simpleText']
            except:
                req_data['subscription'] = ""
                print("Can't able to parse subscription.")

            try:
                req_data['comment_count'] = data[3]['itemSectionRenderer']['contents'][0]['commentsEntryPointHeaderRenderer']['commentCount']['simpleText']
            except:
                try:
                    req_data['comment_count'] = all_data['engagementPanels'][3]['engagementPanelSectionListRenderer']['header']['engagementPanelTitleHeaderRenderer']['contextualInfo']['runs'][0]['text']
                except:
                    req_data['comment_count'] = ""
                    print("Can't able to parse comment_count.")

            try:
                req_data['like_count'] = data[0]['videoPrimaryInfoRenderer']['videoActions']['menuRenderer']['topLevelButtons'][0]['segmentedLikeDislikeButtonViewModel']['likeButtonViewModel']['likeButtonViewModel']['toggleButtonViewModel']['toggleButtonViewModel']['defaultButtonViewModel']['buttonViewModel']['title']
            except:
                req_data['like_count'] = ""
                print("Can't able to parse like_count.")
        except:
            req_data['subscription'] = ""
            req_data['comment_count'] = ""
            req_data['like_count'] = ""

        req_data['media_type'] = "Shorts" if "shorts" in str(url) else "Video"

        return req_data

    def process_video(self, video_id, content_type):

        print(f"Started scraping for video id: {video_id}")
        if content_type == "videos":
            created_url = f"https://www.youtube.com/watch?v={video_id}"
        else:
            created_url = f"https://www.youtube.com/shorts/{video_id}"

        transcription = self.get_transcript(created_url)

        # Fetch video information
        video_info = self.get_video_info(created_url)

        # Fetch video information
        video_info2 = self.get_video_info2(created_url)

        extracted_row = {
            "Author": video_info['author'],
            "Subscription": video_info2['subscription'],
            "Title": video_info['title'],
            "Comment Count": video_info2['comment_count'],
            "Like Count": video_info2['like_count'],
            "View Count": video_info['view_count'],
            "Media Type": video_info2['media_type'],
            "Length": video_info['length'],
            "Script": transcription,
            "Video URL": created_url
        }

        print(f"Extracted data from video url {created_url}")

        return extracted_row

    def process_video_url(self, youtube_url):

        url = self.extract_url_from_text(youtube_url)

        if url:
            if "shorts" in url:
                content_type = "shorts"
            else:
                content_type = "videos"

            video_id = self.get_video_id(url)

            try:
                return self.process_video(video_id, content_type)
            except Exception as exe:
                print(f"Error: {exe}")
                return None
        else:
            return None
