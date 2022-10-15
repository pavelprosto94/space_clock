import json
def readNotifications():
  notification = {}
  notification['lastseen'] = -1
  notification['tree'] = []
  try:
    with open('/flash/notifications.txt', 'r') as json_file:
      notification = json.load(json_file)
  except Exception as e:
    notification = {}
    notification['lastseen'] = -1
    notification['tree'] = []
  return notification

def clearNotifications():
  notification = {}
  notification['lastseen'] = -1
  notification['tree'] = []
  saveNotifications(notification)

def saveNotifications(notification):
  err=0
  try:
    while notification != readNotifications() and err<99:
      with open('/flash/notifications.txt', 'w') as outfile:
        json.dump(notification, outfile)
      err+=1
    if err==99:
      return False
  except Exception as e:
    print("ERROR saveNotifications:\n"+str(e))
    return False
  return True

def NotificationExist(notification,from_name, body_text, metadata):
  ans=False
  if len(notification['tree'])>0:
    for d in notification['tree']:
      if d['from'] == from_name and d['body'] == body_text and d['metadata']==metadata:
        ans=True
        break
  return ans

def addNotifications(new_notifications):
  notification = readNotifications()
  ind=0
  for n in new_notifications:
    if len(notification['tree'])>0:
      ind = notification['tree'][-1]['id']+1
    from_name=n['from']
    body_text=n['body']
    metadata=n['metadata']
    if not NotificationExist(notification,from_name, body_text, metadata):
      notification['tree'].append({
        'from': from_name,
        'body': body_text,
        'id': ind,
        'metadata': metadata
        })
  if len(notification['tree'])>32:
    notification['tree']=notification[:-30]
  return saveNotifications(notification)

def addNotification(from_name, body_text, metadata=""):
  notification = readNotifications()
  ind=0
  if len(notification['tree'])>0:
    ind = notification['tree'][-1]['id']+1
  if not NotificationExist(notification,from_name, body_text, metadata):
    notification['tree'].append({
      'from': from_name,
      'body': body_text,
      'id': ind,
      'metadata': metadata
      })
  if len(notification['tree'])>32:
    notification['tree']=notification[:-30]
  return saveNotifications(notification)

def removeNotification(id):
  notification = readNotifications()
  if len(notification['tree'])>0:
    for i,d in enumerate(notification['tree']):
      if d['id']==id:
        notification['tree'].pop(i)
        if len(notification['tree'])>0:
          notification['lastseen']=notification['tree'][-1]['id']
        saveNotifications(notification)
        break
      
def seenNotifications():
  notification = readNotifications()
  if len(notification['tree'])>0:
    notification['lastseen']=notification['tree'][-1]['id']
    saveNotifications(notification)

def getUnreadNotificationsCount():
  notification = readNotifications()
  if len(notification['tree'])>0:
    for i,d in enumerate(notification['tree']):
      if d['id']==notification['lastseen']:
        return len(notification['tree'])-1-i
  return len(notification['tree'])