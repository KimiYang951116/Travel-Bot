text = '/detail/ChIJ3cfgKtgBaDQRdUAPzn8Adyo(政大安九食堂-嗶啵)'
information = text.split('/')[2]
placeID = information.split('(')[0]
place_name = information.split('(')[1].split(')')[0]