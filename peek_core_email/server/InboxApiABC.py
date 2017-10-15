from datetime import datetime
from typing import Optional, List

from abc import ABCMeta, abstractmethod


class NewTask:
    """ TaskTuple

    A TaskTuple represents the feature rich mechanism for notifications, alerts and messages
     sent from initiator plugins to mobile devices.

    """

    # Auto complete options, Must match _private.storage.Task.Task.state
    AUTO_COMPLETE_OFF = 0
    AUTO_COMPLETE_ON_DELIVER = 1
    AUTO_COMPLETE_ON_SELECT = 2
    AUTO_COMPLETE_ON_ACTION = 4
    AUTO_COMPLETE_ON_DIALOG = 16

    # Auto delete options, Must match _private.storage.Task.Task.state
    AUTO_DELETE_OFF = 0
    AUTO_DELETE_ON_DELIVER = 1
    AUTO_DELETE_ON_SELECT = 2
    AUTO_DELETE_ON_ACTION = 4
    AUTO_DELETE_ON_COMPLETE = 8
    AUTO_DELETE_ON_DIALOG = 16

    # notification mask (multiple options allowed)
    NOTIFY_BY_DEVICE_POPUP = 1
    NOTIFY_BY_DEVICE_SOUND = 2
    NOTIFY_BY_SMS = 4
    NOTIFY_BY_EMAIL = 8
    NOTIFY_BY_DEVICE_DIALOG = 16

    # Display options
    DISPLAY_AS_TASK = 0
    DISPLAY_AS_MESSAGE = 1

    # Priority options
    PRIORITY_SUCCESS = 1
    PRIORITY_INFO = 2
    PRIORITY_WARNING = 3
    PRIORITY_DANGER = 4

    def __init__(self, uniqueId: str, userId: str, title: str,
                 description: Optional[str] = None, iconPath: Optional[str] = None,
                 displayAs: int = DISPLAY_AS_TASK,
                 displayPriority: int = PRIORITY_SUCCESS,
                 routePath: Optional[str] = None, routeParamJson: Optional[dict] = None,
                 autoComplete: int = AUTO_COMPLETE_OFF,
                 autoDelete: int = AUTO_DELETE_OFF,
                 autoDeleteDateTime: Optional[datetime] = None,
                 onDeliveredPayload: Optional[bytes] = None,
                 onCompletedPayload: Optional[bytes] = None,
                 onDeletedPayload: Optional[bytes] = None,
                 onDialogConfirmPayload: Optional[bytes] = None,
                 notificationRequiredFlags: int = 0,
                 actions: List['NewTaskAction'] = (),
                 overwriteExisting=False):
        """
        :param uniqueId: A unique identifier provided when this task was created.
            The initiating plugin may use this later to cancel the task.
            HINT : Ensure you prefix the uniqueId with your plugin name.
    
        :param userId: A string representing the unique ID of the user. This must match the
            users plugin.
    
        :param title: The title to display in the task.
        :param description: The long text that is displayed under the title for this task.
        :param iconPath: The URL for the icon, if any.
        :param displayAs: Should this task be displayed as a message or task?
        :param displayPriority: What priority should the task display as?
    
        :param routePath: If this route path is defined, then selecting the task
            will cause the peek client fe to change routes to a new page.
        :param routeParamJson: If the route path is defined, this route param json 
            will be passed along when the route is switched..
    
        :param autoComplete: Should this task auto complete?
                This parameter defines what state it will auto complete in.
                See the AUTO_COMPLETE... class constants
        :param autoDelete: Should this task auto delete?
                This parameter defines what state it will auto delete in.
                See the AUTO_DELETE... class constants
        :param autoDeleteDateTime: The datetime when this task should automatically
                be deleted it if still exists.
    
        :param onDeliveredPayload: (Optional) The payload that will be delivered locally
            on Peek Server when the task is delivered.
        :param onCompletedPayload: (Optional) The payload that will be delivered locally
            on Peek Server when the task is completed (auto, or otherwise)
        :param onDeletedPayload: (Optional) The payload that will be delivered locally
            on Peek Server when the task is deleted (auto, or otherwise)
        :param onDialogConfirmPayload: (Optional) The payload that will be delivered
            locally on Peek Server when the user clicks "OK" on the dialog.
            
        :param overwriteExisting: If a task with that uniqueId already exists, it will be
            deleted.
        """
        self.uniqueId = self._required(uniqueId, "uniqueId")
        self.userId = self._required(userId, "userId")

        # The display properties of the task
        self.title = self._required(title, "title")
        self.description = description
        self.iconPath = iconPath

        self.displayAs = displayAs
        self.displayPriority = displayPriority
        if not self.displayPriority in (1, 2, 3, 4):
            raise Exception("Invalid displayPriority %s" % self.displayPriority)

        # The mobile-app route to open when this task is selected
        self.routePath = routePath
        self.routeParamJson = routeParamJson

        # The confirmation options
        self.onDeliveredPayload = onDeliveredPayload
        self.onCompletedPayload = onCompletedPayload
        self.onDeletedPayload = onDeletedPayload
        self.onDialogConfirmPayload = onDialogConfirmPayload

        self.autoComplete = autoComplete
        self.autoDelete = autoDelete
        self.autoDeleteDateTime = autoDeleteDateTime
        self.overwriteExisting = overwriteExisting

        self.notificationRequiredFlags = notificationRequiredFlags

        # The actions for this TaskTuple.
        self.actions = list(actions)

    def _required(self, val, desc):
        if not val:
            raise Exception("%s is not optional" % desc)

        return val


class NewTaskAction:
    """ TaskTuple Action

    This object represents the TaskTuple Actions.
    Tasks have zero or more actions that can be performed by the user when they
    receive a task.

    """

    def __init__(self, title: str, confirmMessage: str,
                 onActionPayload: Optional[bytes] = None):
        """
        :param title: The title of the action, this will appear as a menu option.
        :param confirmMessage: This is the message that will be shown to confirm the action.
        :param onActionPayload: This payload will be delivered locally on Peek Server
                 When the action is performed on the user device.
        """
        self.title = self._required(title, "title")
        self.confirmMessage = self._required(confirmMessage, "confirmMessage")
        self.onActionPayload = self._required(onActionPayload, "onActionPayload")

    def _required(self, val, desc):
        if not val:
            raise Exception("%s is not optional" % desc)

        return val


class NewActivity:
    """ TaskTuple

    A TaskTuple represents the feature rich mechanism for notifications, alerts and messages
     sent from initiator plugins to mobile devices.

    """

    def __init__(self, uniqueId: str, userId: str, title: str,
                 autoDeleteDateTime: datetime,
                 dateTime: Optional[datetime] = None,
                 description: Optional[str] = None, iconPath: Optional[str] = None,
                 routePath: Optional[str] = None, routeParamJson: Optional[dict] = None,
                 overwriteExisting=False):
        """

        :param uniqueId: A unique identifier provided when this task was created.
            The initiating plugin may use this later to cancel the task.
            HINT : Ensure you prefix the uniqueId with your plugin name.
    
        :param userId: A string representing the unique ID of the user. This must match the
            users plugin.
    
        :param title: The title to display in the task.
        :param description: The long text that is displayed under the title for this task.
        :param iconPath: The URL for the icon, if any.
    
        :param routePath: If this route path is defined, then selecting the task
            will cause the peek client fe to change routes to a new page.
        :param routeParamJson: If the route path is defined, this route param json 
            will be passed along when the route is swtiched.
            
        :param autoDeleteDateTime: The time and date when this activity will be deleted.
            
        :param overwriteExisting: If an activity with that uniqueId already exists,
            it will be deleted.
        
        """
        self.uniqueId = self._required(uniqueId, "uniqueId")
        self.userId = self._required(userId, "userId")
        self.dateTime = dateTime if dateTime else datetime.utcnow()

        # The display properties of the task
        self.title = self._required(title, "title")
        self.description = description
        self.iconPath = iconPath

        # The mobile-app route to open when this item is selected
        self.routePath = routePath
        self.routeParamJson = routeParamJson

        # Auto Delete on Time
        self.autoDeleteDateTime = autoDeleteDateTime

        self.overwriteExisting = overwriteExisting

    def _required(self, val, desc):
        if not val:
            raise Exception("%s is not optional" % desc)

        return val


class InboxApiABC(metaclass=ABCMeta):
    @abstractmethod
    def addTask(self, task: NewTask) -> None:
        """ Add a New Task

        Add a new task to the users device.
        
        :param task: The definition of the task to add.
        
        """

    @abstractmethod
    def completeTask(self, uniqueId: str) -> None:
        """ Complete a Task
        
        Mark a task as complete. NOTE, This doesn't delete it.
        
        :param uniqueId: The uniqueId provided when the task was created.
        """

    @abstractmethod
    def removeTask(self, uniqueId: str) -> None:
        """ Remove a Task
        
        Remove a task from the users device.
        
        :param uniqueId: The uniqueId provided when the task was created.
        """

    @abstractmethod
    def addActivity(self, activity: NewActivity) -> None:
        """ Add a new Activity item

        Add a new Activity to the users device.

        :param activity: The definition of the activity to add.

        """

    @abstractmethod
    def removeActivity(self, uniqueId: str) -> None:
        """ Remove an Activity item

        Remove an Activity from the users device.

        :param uniqueId: The uniqueId provided when the activity was created.
        """
