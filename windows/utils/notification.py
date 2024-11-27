from pyqttoast import Toast, ToastPreset, ToastPosition
from utils.assets import is_dark_theme

def notification(parent, message, message_type = "SUCCESS"):
    Toast.setPosition(ToastPosition.TOP_MIDDLE)
    Toast.setPositionRelativeToWidget(parent)
    Toast.setOffset(30, 10)
    toast = Toast(parent)
    toast.setDuration(2000)
    toast.setText(message)
    toast.setShowDurationBar(False)
    toast.setShowIconSeparator(False)
    toast.setShowCloseButton(False)
    toast.setResetDurationOnHover(False)
    if message_type == "SUCCESS":
        if is_dark_theme():
            toast.applyPreset(ToastPreset.SUCCESS_DARK)
        else:
            toast.applyPreset(ToastPreset.SUCCESS)
    else:
        if is_dark_theme():
            toast.applyPreset(ToastPreset.ERROR_DARK)
        else:
            toast.applyPreset(ToastPreset.ERROR)
    toast.show()