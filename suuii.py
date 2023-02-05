import pickle
import numpy as np
model = pickle.load(open('model.pkl','rb'))
a=[1,1,1,1,1,1,1,1]
a=[np.array(a)]
print(model.predict(a))