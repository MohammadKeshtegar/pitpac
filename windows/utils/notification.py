from pyqttoast import Toast, ToastPreset, ToastPosition

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
        toast.applyPreset(ToastPreset.SUCCESS_DARK)
    elif message_type == "ERROR":
        toast.applyPreset(ToastPreset.ERROR_DARK)
    toast.show()