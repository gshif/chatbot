import pytest
import random
import re
from websocket import enableTrace
from lib.setup_logger import logger


# enable trace
enableTrace(True)
# reminder seconds list
ADD_REMINDER_TIME = ["a", "an", "0", "1", "-1", "10", "10000", "1000000", "1000000000", "n", "1!"]
ADD_REMINDER_UNIT = ["second", "seconds", "minute", "minutes", "hour", "hours"]
ADD_REMINDER_MESSAGE = ["remind me to", "tell me to"]
BUF_SIZE_BYTES = 10000000
# encoding chardet.detect(b)["encoding"] = Windows-1254


# test header
def header(test_name):
    logger.info('#' * (11 + len(test_name) + 17))
    logger.info('<--------- {} START --------->'.format(test_name))
    logger.info('#' * (11 + len(test_name) + 17))


# test footer
def footer(test_name):
    logger.info('#' * (11 + len(test_name) + 15))
    logger.info('<--------- {} END --------->'.format(test_name))
    logger.info('#' * (11 + len(test_name) + 15) + "\n")


@pytest.mark.usefixtures("connect")
class TestReminders(object):
    """ TODO """
    @pytest.mark.add_reminder
    @pytest.mark.parametrize("quantity", ADD_REMINDER_TIME)
    @pytest.mark.parametrize("unit", ADD_REMINDER_UNIT)
    @pytest.mark.parametrize("reminder", ADD_REMINDER_MESSAGE)
    def test_add_reminders_with_remind_and_tell(self, reminder, quantity, unit):
        """ TODO """
        test_name = f"test_add_reminders_with_remind_and_tell{quantity}_{unit}_{reminder}"
        message_text = "go to sleep"
        expected_response = ""
        # build a message to send
        message_to_send = f"{reminder} {message_text} in {quantity} {unit}"
        if quantity.isdigit():
            if unit in ["second", "seconds"]:
                quantity_seconds = quantity
                logger.info(f"quantity_seconds : {quantity_seconds}")
                if quantity_seconds == "1":
                    expected_response = f"Ok, I will remind you to {message_text} in 1 second."
                else:
                    expected_response = f"Ok, I will remind you to {message_text} in {quantity_seconds} seconds."
            elif unit in ["minute", "minutes"]:
                quantity_seconds = int(quantity) * 60
                if quantity == "1":
                    expected_response = f"Ok, I will remind you to {message_text} in 60 seconds"
                else:
                    expected_response = f"Ok, I will remind you to {message_text} in {quantity_seconds} seconds."
            elif unit in ["hour", "hours"]:
                quantity_seconds = int(quantity) * 3600
                if quantity == "1":
                    expected_response = f"Ok, I will remind you to {message_text} in 3600 seconds."
                else:
                    expected_response = f"Ok, I will remind you to {message_text} in {quantity_seconds} seconds."
            # special case with 'a' and 'an' without a number/digit, should be translated to 1, in this test, hour
        else:
            if quantity in ["a", "an"]:
                if unit in ["second", "seconds"]:
                    expected_response = f"Ok, I will remind you to {message_text} in 1 second."
                elif unit in ["minute", "minutes"]:
                    expected_response = f"Ok, I will remind you to {message_text} in 60 seconds."
                elif unit in ["hour", "hours"]:
                    expected_response = f"Ok, I will remind you to {message_text} in 3600 seconds."
            else:
                expected_response = f"I'm sorry, I don't understand what you mean."
        header(test_name)
        logger.debug(f"Assert Websocket connection is up.")
        assert self.connect.connected, f"{test_name}: Websocket is not connected."
        logger.info(f"Step 1: Send message to add reminder : \"{message_to_send}\"")
        self.connect.send(message_to_send)
        logger.info(f"Step 2: Verify server response.")
        actual_server_response = self.connect.frame_buffer.recv(bufsize=BUF_SIZE_BYTES)
        logger.debug(f"not parsed actual server response : {actual_server_response}")
        # actual_server_response is of type = bytes, need to convert to string and replace some of the characters.
        s_actual_server_response = actual_server_response.decode("unicode-escape").encode("ascii", "ignore") \
            .decode("ascii", "ignore")
        logger.debug(f"actual server response : {s_actual_server_response}")
        logger.info(f"Assert expected server response \"{expected_response}\" in "
                    f"actual server response \"{s_actual_server_response}\"")
        assert expected_response in s_actual_server_response, \
            f"ERROR, expected server response \"{expected_response}\" differs from " \
            f"actual server response \"{s_actual_server_response}\""
        footer(test_name)

    @pytest.mark.list_reminders
    @pytest.mark.parametrize("what", ["", "me", "all", "of", "my"])
    @pytest.mark.parametrize("list_reminders", ["list", "show", "tell"])
    def test_list_reminders(self, list_reminders, what):
        """ TODO """
        test_name = f"test_list_reminders_{list_reminders}_{what} "
        reminder_message = ["remind me to", "tell me to"]
        text_message = ["go to sleep", "go to eat"]
        time_m = 100
        unit = ["seconds", "minutes", "hours"]
        if not what:
            list_message = f"{list_reminders} reminders."
        else:
            list_message = f"{list_reminders} {what} reminders."
        expected_count_of_reminders = 10

        header(test_name)
        # send 10 messages
        logger.info(f"{test_name} : Step 1 - Send 10 reminder messages.")
        for i in range(1,11):
            message_to_send = f"{random.choice(reminder_message)} {random.choice(text_message)} in " \
                              f"{time_m} {random.choice(unit)}"
            logger.debug(f"{test_name} : {message_to_send}")
            # make sure there is a websocket connection
            assert self.connect.connected, f"websocket is not connected"
            # send a reminder message
            logger.info(f"{test_name} : Sending message \"{i}\" -> {message_to_send}")
            self.connect.send(message_to_send)
            # get all the responses from the server
            actual_server_response = self.connect.frame_buffer.recv(bufsize=BUF_SIZE_BYTES)
            logger.debug(f"not parsed actual server response : {actual_server_response}")
        logger.info(f"{test_name} : Step 2 - List all of the sent messages")
        self.connect.send(list_message)
        actual_server_response = self.connect.frame_buffer.recv(bufsize=BUF_SIZE_BYTES)
        s_actual_server_response = actual_server_response.decode("unicode-escape").encode("ascii", "ignore")\
            .decode("ascii", "ignore")
        logger.debug(f"{test_name} : actual server response -> {s_actual_server_response}")
        # parse the returned list
        list_of_reminders = re.findall(r"<td>(\d+)</td>\n\s+<td>(\d+)</td>\n\s+<td>([a-zA-Z ]+)</td>\n",
                                       s_actual_server_response)
        logger.debug(f"{test_name} : {list_of_reminders}")
        assert len(list_of_reminders) == 10, \
            f"Assertion Error : Expected count of reminders {expected_count_of_reminders} does not equal to Actual " \
            f"count of reminders {len(list_of_reminders)}"
        footer(test_name)

    @pytest.mark.delete_reminders
    @pytest.mark.parametrize("what", ["", "all","of", "my"])
    @pytest.mark.parametrize("remove_reminders", ["clear", "delete", "remove", "forget"])
    def test_delete_reminders(self, remove_reminders, what):
        """ TODO """

        test_name = f"test_delete_reminders_{remove_reminders}_{what} "
        reminder_message = ["remind me to", "tell me to"]
        text_message = ["go to sleep", "go to eat"]
        time_m = 100
        unit = ["seconds", "minutes", "hours"]
        if not what:
            delete_message = f"{remove_reminders} reminders."
        else:
            delete_message = f"{remove_reminders} {what} reminders."
        expected_delete_response = "Ok, I have cleared all of your reminders."
        expected_list_response = "You have no reminders."
        list_of_reminders = ["list", "show", "tell"]
        list_message = f"{random.choice(list_of_reminders)} reminders"

        header(test_name)
        # send 10 messages
        logger.info(f"{test_name} : Step 1 - Send 10 reminder messages.")
        for i in range(1,11):
            message_to_send = f"{random.choice(reminder_message)} {random.choice(text_message)} in " \
                              f"{time_m} {random.choice(unit)}"
            logger.debug(f"{test_name} : {message_to_send}")
            # make sure there is a websocket connection
            assert self.connect.connected, f"websocket is not connected"
            # send a reminder message
            logger.info(f"{test_name} : Sending message \"{i}\" -> {message_to_send}")
            self.connect.send(message_to_send)
            # get all the responses from the server
            actual_server_response = self.connect.frame_buffer.recv(bufsize=BUF_SIZE_BYTES)
            logger.debug(f"not parsed actual server response : {actual_server_response}")
        logger.info(f"{test_name} : Step 2 - Remove all of the existing reminders")
        self.connect.send(delete_message)
        actual_delete_response = self.connect.frame_buffer.recv(bufsize=BUF_SIZE_BYTES)
        s_actual_delete_response = actual_delete_response.decode("unicode-escape").encode("ascii", "ignore")\
            .decode("ascii", "ignore")
        logger.debug(f"{test_name} : actual server response -> {s_actual_delete_response}")
        logger.info(f"{test_name} : Assert expected server response \"{expected_delete_response}\" in "
                    f"actual server response \"{s_actual_delete_response}\"")
        assert expected_delete_response in s_actual_delete_response, \
            f"ERROR, expected server response \"{expected_delete_response}\" differs from " \
            f"actual server response \"{s_actual_delete_response}\""
        # get all reminders to make sure there are none...
        logger.info(f"{test_name} : Step 3 - List reminders")
        self.connect.send(list_message)
        actual_list_response = self.connect.frame_buffer.recv(bufsize=BUF_SIZE_BYTES)
        s_actual_list_response = actual_list_response.decode("unicode-escape").encode("ascii", "ignore") \
            .decode("ascii", "ignore")
        logger.debug(f"{test_name} : actual server response -> {s_actual_list_response}")
        logger.info(f"{test_name} : Assert expected server response \"{expected_list_response}\" in "
                    f"actual server response \"{s_actual_list_response}\"")
        assert expected_list_response in s_actual_list_response, \
            f"ERROR, expected server response \"{expected_list_response}\" differs from " \
            f"actual server response \"{s_actual_list_response}\""
        footer(test_name)

    @pytest.mark.delete_specific_reminder
    @pytest.mark.parametrize("reminder_id", ["1", "2", "10"])
    @pytest.mark.parametrize("reminder", ["", "reminder"])
    @pytest.mark.parametrize("remove_reminders", ["clear", "delete", "remove", "forget"])
    def test_delete_specific_reminder(self, remove_reminders, reminder, reminder_id):
        """ TODO """
        test_name = f"test_delete_specific_reminder_{remove_reminders}_{reminder} "
        reminder_message = ["remind me to", "tell me to"]
        text_message = "go to sleep"
        time_m = 100
        unit = ["seconds", "minutes", "hours"]
        # initialize reminder id to be removed
        reminder_id = reminder_id
        expected_count_of_reminders = 9
        if not reminder:
            delete_message = f"{remove_reminders} {reminder_id}"
        else:
            delete_message = f"{remove_reminders} {reminder} {reminder_id}"
        expected_delete_response = f"Ok, I will not remind you to {text_message}."
        list_of_reminders = ["list", "show", "tell"]
        list_message = f"{random.choice(list_of_reminders)} reminders"

        header(test_name)
        # send 10 messages
        logger.info(f"{test_name} : Step 1 - Send 10 reminder messages.")
        for i in range(1, 11):
            message_to_send = f"{random.choice(reminder_message)} {text_message} in " \
                              f"{time_m} {random.choice(unit)}"
            logger.debug(f"{test_name} : {message_to_send}")
            # make sure there is a websocket connection
            assert self.connect.connected, f"websocket is not connected"
            # send a reminder message
            logger.info(f"{test_name} : Sending message \"{i}\" -> {message_to_send}")
            self.connect.send(message_to_send)
            # get all the responses from the server
            actual_server_response = self.connect.frame_buffer.recv(bufsize=BUF_SIZE_BYTES)
            logger.debug(f"not parsed actual server response : {actual_server_response}")
        logger.info(f"{test_name} : Step 2 - Remove reminder id {reminder_id}")
        self.connect.send(delete_message)
        actual_delete_response = self.connect.frame_buffer.recv(bufsize=BUF_SIZE_BYTES)
        s_actual_delete_response = actual_delete_response.decode("unicode-escape").encode("ascii", "ignore")\
            .decode("ascii", "ignore")
        logger.debug(f"{test_name} : actual server response -> {s_actual_delete_response}")
        logger.info(f"{test_name} : Assert expected server response \"{expected_delete_response}\" in "
                    f"actual server response \"{s_actual_delete_response}\"")
        assert expected_delete_response in s_actual_delete_response, \
            f"ERROR, expected server response \"{expected_delete_response}\" differs from " \
            f"actual server response \"{s_actual_delete_response}\""
        # get all reminders to make sure there are none...
        logger.info(f"{test_name} : Step 3 - List reminders")
        self.connect.send(list_message)
        actual_list_response = self.connect.frame_buffer.recv(bufsize=BUF_SIZE_BYTES)
        s_actual_list_response = actual_list_response.decode("unicode-escape").encode("ascii", "ignore") \
            .decode("ascii", "ignore")
        list_of_reminders = re.findall(r"<td>(\d+)</td>\n\s+<td>(\d+)</td>\n\s+<td>([a-zA-Z ]+)</td>\n",
                                       s_actual_list_response)
        logger.debug(f"{test_name} : {list_of_reminders}")
        assert len(list_of_reminders) == expected_count_of_reminders, \
            f"Assertion Error : Expected count of reminders {expected_count_of_reminders} does not equal to Actual " \
            f"count of reminders {len(list_of_reminders)}"
        footer(test_name)