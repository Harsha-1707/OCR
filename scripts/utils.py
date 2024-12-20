import cv2
from skimage.feature import hog

def preprocess_and_extract_features(img_path):
    img = cv2.imread(img_path)
    img_res = cv2.resize(img, (64, 128), interpolation=cv2.INTER_AREA)
    img_gray = cv2.cvtColor(img_res, cv2.COLOR_BGR2GRAY)
    hog_img = hog(img_gray, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(1, 1))
    return hog_img

def load_model(model_path='models/ocr_model.pkl'):
    import joblib
    return joblib.load(model_path)
