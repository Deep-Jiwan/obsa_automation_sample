# Obs_Controlling Python Script.
import obsws_python as obs
import time
import datetime
from configparser import ConfigParser
import logging
import asyncio
import telegram
import webbrowser

# Open the config file for varibles. 
file='config.ini'
config=ConfigParser()
config.read(file)

# Variable assignment from the config file      
ws_host=config["websocket_settings"]["host"]
ws_port=config["websocket_settings"]["port"]
ws_password=config["websocket_settings"]["password"]
stream_server= config["stream_settings"]["streamserver"]
stream_key= config["stream_settings"]["streamkey"]
yt_std  = config["stream_settings"]["yt_std"]
hours = int(config["run_time"]["hours"])
mins = int(config["run_time"]["mins"])
secs= int(config["run_time"]["secs"])
run_time = (hours*60*60) + (mins*60) + secs
output_record =eval(config["output_options"]["output_record"])
output_stream =eval(config["output_options"]["output_stream"])
hold_time = int(config["run_time"]["hold_time"])
overtime = int(config["run_time"]["overtime"])
tele_enable = eval(config["telegram"]["enable"])
if tele_enable == True:
    key= config["telegram"]["key"]
    chat_id= int(config["telegram"]["chatid"])


######################################################################

# Open Youtube Studio / Any other streaming service
if output_stream == True:
    webbrowser.open_new_tab(yt_std)
    time.sleep(10)

# Create a logger object
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a file handler and set the level to DEBUG
file_handler = logging.FileHandler('obsrun_logs.log',mode="w")
file_handler.setLevel(logging.DEBUG)

# Create a console handler and set the level to INFO
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatters and add it to the handlers
debug_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(debug_formatter)

info_formatter = logging.Formatter('%(message)s')
console_handler.setFormatter(info_formatter)

# Add a filter so that passwords are not logged.
class PasswordFilter(logging.Filter):
    def filter(self, record):
        return "password" not in record.getMessage()

# Add the filter to the handlers
file_handler.addFilter(PasswordFilter())
console_handler.addFilter(PasswordFilter())

# Set up a handler to send messages to the Tele bot
class TelegramHandler(logging.Handler):
    def __init__(self, bot_token, chat_id):
        super().__init__()
        self.bot_token = bot_token
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        bot = telegram.Bot(token=self.bot_token)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        asyncio.run(self.send_telegram_message(bot, log_entry))
        
    async def send_telegram_message(self, bot, log_entry):
        await bot.send_message(chat_id=self.chat_id, text=log_entry)

# Initialize the bot and the handler
if tele_enable == True:
    bot_token = key
    telegram_handler = TelegramHandler(bot_token, chat_id)
    logger.addHandler(telegram_handler)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Time and date function
def gettime(a):
    '''
    Get current date and time Function
    Case 1, a = 1 : Prints date and time with "Started"
    Case 2, a = 2 : Prints date and time with "Ended" 
    '''
    st_time =datetime.datetime.now()
    st_time =st_time.strftime('%y-%m-%d %H:%M:%S')
    if a==1:
        logger.info(f"Started at {st_time}\n")
    else:
        logger.info(f"Ended at {st_time}\n\n\n\n\n")

def terminate_session(overtime):
    '''
    Checks if long_session is in program.
    If True, session will continue for overtime minutes.
    If False, Nothing will be executed, Script will continue.
    Accepts Overtime in minutes
    '''
    overtime = overtime*60 # overtime is now in seconds
    program_scene = cl.get_current_program_scene().__dict__["current_program_scene_name"]
    chk_overtime = 0
    # session goes on while Long session is in program and we are under the overtime limit
    while program_scene == "Over_Time" and chk_overtime <= overtime:
        time.sleep(1) # Makes the code run every 1 second only
        program_scene = cl.get_current_program_scene().__dict__["current_program_scene_name"] 

        # To Print once a min about overtime
        if ".0 " in (f"{chk_overtime/60} "): # Yeah this is the most jankiest code ever lol! Using &nbsp to filter perfect divisions 
            logger.info(f"Overtime session in progress. \n{int((overtime-chk_overtime)/60)} Minutes until session ends\n")
        chk_overtime+=1
    else:
        logger.info("session will end soon")
        

# User awareness text

logger.info("\nHellow there!,")
logger.info("\nATTENTION: THIS IS AN AUTOMATED STREAM,")

# Prints out the time and date of starting
gettime(1) 


# Connecting to OBS Websocket
while True:
    try:
        # Connecting to OBS_Ws
        cl = obs.ReqClient(host=ws_host, port=ws_port, password=ws_password)
        logger.info("Connected to OBS Successfully!")
        break
    except TimeoutError as e:
        logger.info(e)
        logger.info(f"Please check if IP Address is set properly and restart \n")
        time.sleep(3)
    except ConnectionRefusedError as e:
        logger.info(e)
        logger.info("\nMake sure OBS is running? \n ")
        logger.info(f" Or Incorrect Port. Use port '{ws_port}' in OBS\n")
        time.sleep(1)
    except obs.error.OBSSDKError as e:
        logger.info("Incorrect Password. Trying again. \n")
        time.sleep(5)

# So port is given priority. OBS must use port set by user
# IP Address : Script must use Target machine IP Address. Restart required is invalid IP is used

# OBS Settings Dictionaries       
p1_stream={
    "server":stream_server,
    "key":stream_key
}
# Below Settings are not use currently but worth trying in the future!
stream_settings  = {
    "Encoder":"x264",
    "Rate Control":"CBR",
    "Bitrate":"3000"
}
rec_settings={
    "Type":"Standard",
    "Recording Format":"mkv"
}
###### End of Variable assignments and Functions #############

#############################################################
########         Running Start Here         #################
#############################################################

# Recalling the scene collection: Sunday session
cl.set_current_scene_collection("sundaysession")
logger.info("\nSetting the Scene\n")
time.sleep(1) # Delay for obs processing
# Sends Holding slide to OBS Program.
cl.set_current_program_scene("holding_slide")

############## FUTURE PROBLEM ####################################
#time.sleep(1)
#cl.set_output_settings(name="Streaming",settings=stream_settings)
#time.sleep(1)
#cl.set_output_settings(name="Recording", settings=rec_settings)
############## FUTURE PROBLEM ####################################

# Streaming and Recording 
    # User awareness text.
logger.info(f'Streaming is set to: {output_stream} and Recording is set to: {output_record} \n')

if output_stream == True:
    # Sets the streaming settings and Stream settings only change if streaming is set True
    cl.set_stream_service_settings(ss_type="rtmp_custom", ss_settings=p1_stream)
    time.sleep(1)
    try:
        cl.start_stream()
    except:
        pass
    logger.info("Youtbe Live Started\n")

time.sleep(1) # Time delay for Streaming to Start

if output_record==True:
    try:
        cl.start_record()
    except:
        pass
    logger.info("HLS / Recording Started\n")


logger.info("Starting the session now!\n")

# Sends Holding slide to OBS Program for Hold time set by user
cl.set_current_program_scene("holding_slide")
logger.info(f"Holding Slide Live for {hold_time} seconds!")
time.sleep(hold_time)

# Sends PGM_main to OBS Program (Main Stream)
cl.set_current_program_scene(name="PGM_main")
logger.info("\nPGM Live\n")

# session will run for the seconds set by user
logger.info(f"session will run for {hours} Hrs and {mins} Mins \n")
time.sleep(run_time)

# After session run time has reached 0 seconds.
# If Long_session is in Program, Stream will not end.

terminate_session(overtime)

# Sends Holding Slide to OBS Program for hold time
cl.set_current_program_scene(name="holding_slide")
logger.info(f"Holding slide live for {hold_time} seconds\n")
time.sleep(hold_time)

# session over and terminal code.
logger.info("session has ended\n")

# Depending on settings, Stream and Recording will be stopped
# You can also do cl.get_record_status().output_active -> dict just gives clarify of use
if cl.get_record_status().__dict__["output_active"] == True:
    cl.stop_record()
    logger.info("Recording has stopped")
if cl.get_stream_status().__dict__["output_active"] == True:
    cl.stop_stream()
    logger.info("Streaming has stopped")
logger.info("Thank you :), Glad i could  help you today\n")

a=0     # a =0 just says that when you print time, say ended instead of started
gettime(a)

# Congrats on reaching the end of this code!
# More features coming soon