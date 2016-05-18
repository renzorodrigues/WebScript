import datetime, os, shutil
from flask import Flask, render_template, request, Response
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES 

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

destination = r'/home/renzo/Imagens/Destino'
temp_dir = r'/home/renzo/Flask/wallpaper/static/img'
wallpaper = 'wallpaper.jpg'

app.config['UPLOADED_PHOTOS_DEST'] = temp_dir
configure_uploads(app, photos)

@app.route('/wallpaper', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST' and 'photo' in request.files:
		filename = photos.save(request.files['photo'], name=wallpaper)
		check = request.form.getlist('check')
		return change_wallpaper(check)
	return render_template('wallpaper.html', destination=os.walk(destination))

def change_wallpaper(check):
	date = datetime.datetime.now()
	
	def generate():
		if os.path.exists(destination+'/'+wallpaper):
			os.rename(os.path.join(destination, wallpaper), os.path.join(destination, 'Wallpaper_'+date.strftime('%H%M%S__%d_%m_%Y')+'.jpg'))

		shutil.copy(os.path.join(temp_dir, wallpaper), destination)
		yield "copiando para " + str(destination) + "\n\n"
	
		for cada in check:
			dirs = cada
			if os.path.exists(dirs+'/'+wallpaper):
				os.rename(os.path.join(dirs, wallpaper), os.path.join(dirs, 'Wallpaper_'+date.strftime('%H%M%S__%d_%m_%Y')+'.jpg'))
			
			shutil.copy(os.path.join(temp_dir, wallpaper), dirs)
			yield "copiando para " + str(dirs) + "\n\n"
	
		os.remove(temp_dir+"/"+wallpaper)
	return render_template('response.html', generate=generate())

if __name__ == '__main__':
	app.run(debug=True)