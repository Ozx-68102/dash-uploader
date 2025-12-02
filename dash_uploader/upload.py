import uuid

from dash_uploader._build.Upload_ReactComponent import Upload_ReactComponent
import dash_uploader.settings as settings

DEFAULT_STYLE = {
    "width": "100%",
    # min-height and line-height should be the same to make
    # the centering work.
    "minHeight": "100px",
    "lineHeight": "100px",
    "textAlign": "center",
    "borderWidth": "1px",
    "borderStyle": "dashed",
    "borderRadius": "7px",
}


def update_upload_api(requests_pathname_prefix, upload_api):
    """Path join for the API path name.
    This is a private method, and should not be exposed to users.
    """
    if requests_pathname_prefix == "/":
        return upload_api
    return "/".join(
        [
            requests_pathname_prefix.rstrip("/"),
            upload_api.lstrip("/"),
        ]
    )


def combine(overriding_dict, base_dict):
    """Combining two dictionaries without modifying them.
    This is a private method, and should not be exposed to users.
    """
    if overriding_dict is None:
        return dict(base_dict)
    return {**base_dict, **overriding_dict}


# Implemented as function, but still uppercase.
# This is because subclassing the Dash-auto-generated
# "Upload from Upload.py" will give some errors
def Upload(
    id: str="dash-uploader",
    text: str="Drag and Drop Here to upload!",
    text_completed: str="Uploaded: ",
    text_completed_no_suffix: bool=False,
    text_disabled: str="The uploader is disabled.",
    cancel_button: bool=True,
    pause_button: bool=False,
    disabled: bool=False,
    filetypes: list[str] | None=None,
    max_file_size: int=1024,
    max_total_size: int=5 * 1024,
    chunk_size: int=1,
    default_style: dict[str, str] | None=None,
    upload_id: str | None=None,
    max_files: int=1,
    failed_files: list[str]=None,
    is_uploading: bool=False,
):
    """
    du.Upload component

    Parameters
    ----------
    id: str
        The id of the du.Upload component.
    text: str
        The text to show in the upload "Drag
        and Drop" area. Optional.
    text_completed: str
        The text to show in the upload area
        after upload has completed successfully before
        the name of the uploaded file. For example, if user
        uploaded "data.zip" and `text_completed` is
        "Ready! ", then user would see text "Ready!
        data.zip".
    text_completed_no_suffix: bool (default: False)
        If True, do not append the filename to the completed message.
        Only show the text defined in 'text_completed' without appending
        the uploaded filename.
    text_disabled: str
        The text to show in the upload area when the component
        is disabled.
    cancel_button: bool
        If True, shows a cancel button.
    pause_button: bool
        If True, shows a pause button.
    disabled: bool
        If True, the file is not allowed to be uploaded.
    filetypes: list of str or None
        The filetypes that can be uploaded.
        For example: ['zip', 'rar'] or ['.csv', '.Excel'].

        Notes:
        - Case insensitive ('zip' == 'ZIP').
        - The leading dot is optional ('jpg' == '.jpg').
        - This just checks the extension of the filename. Users might
          still upload any kind of file by renaming it!
        - By default, all filetypes are accepted.
    max_file_size: numeric
        The maximum file size in Megabytes. Optional.
        Default: 1024 (1Gb).
    max_total_size: numeric
        The maximum total size of files to be uploaded
        in Megabytes. Default: 5*1024 (5Gb)
    chunk_size: numeric
        The chunk size in Megabytes. Optional.
    default_style: None or dict
        Inline CSS styling for the main div element.
        If None, use the default style of the component.
        If dict, will use the union on the given dict
        and the default style. (you may override
        part of the style by giving a dictionary)
        More styling options through the CSS classes.
    upload_id: None or str
        The upload id, created with uuid.uuid1() or uuid.uuid4(),
        for example. If none, creates random session id with
        uuid.uuid1().
    max_files: int (default: 1)
        EXPERIMENTAL feature. Read below. For bulletproof
        implementation, force usage of zip files and keep
        max_files = 1.

        The number of files that can be added to
        the upload field simultaneously.

        Notes:
        (1) If even a single file which is not supported file
         type, is added to the upload queue, upload process of
         all files will be permanently interrupted.
        (2) Use reasonably small amount in "max_files".
        (3) When uploading two folders with Chrome, there is
         a bug in resumable.js which makes only one of the
         folders to be uploaded. See:
         https://github.com/23/resumable.js/issues/416
        (4) When uploading folders, note that the subdirectories
          are NOT created -> All files in the folders will
          be uploaded to the single upload folder.
    failed_files: list of str (default: None)
        A list of filenames that failed to upload.
        Typically used as an Output/State in callbacks, but can be
        initialized here if needed.
    is_uploading: bool (default: False)
        Indicates whether the upload process is currently active.
        Can be used as an Input in Dash callbacks to disable/enable
        other components during upload.

    Returns
    -------
    Upload: dash component
        Initiated Dash component for app.layout.
    """

    # Handle styling
    default_style = combine(default_style, DEFAULT_STYLE)
    disabled_style = combine({"opacity": "0.5"}, default_style)
    upload_style = combine({"lineHeight": "0px"}, default_style)

    if upload_id is None:
        upload_id = uuid.uuid1()

    service = update_upload_api(settings.requests_pathname_prefix, settings.upload_api)

    arguments = dict(
        id=id,
        dashAppCallbackBump=0,
        # Have not tested if using many files
        # is reliable -> Do not allow
        maxFiles=max_files,
        maxTotalSize=max_total_size * 1024 * 1024,
        maxFileSize=max_file_size * 1024 * 1024,
        chunkSize=chunk_size * 1024 * 1024,
        text=text,
        service=service,
        startButton=False,
        disabled=disabled,
        # Not tested so default to one.
        simultaneousUploads=1,
        completedMessage=text_completed,
        disabledMessage=text_disabled,
        cancelButton=cancel_button,
        pauseButton=pause_button,
        defaultStyle=default_style,
        disabledStyle=disabled_style,
        uploadingStyle=upload_style,
        completeStyle=default_style,
        upload_id=str(upload_id),
        totalFilesCount=0,
        failedFileNames=failed_files if failed_files is not None else [],
        isUploading=is_uploading,
        completedMessageNoSuffix=text_completed_no_suffix,
    )

    if filetypes:
        arguments["filetypes"] = filetypes

    return Upload_ReactComponent(**arguments)
