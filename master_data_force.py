# -*- coding: utf-8 -*-
"""master_data_force.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZhDlhqHISAqFYiFQzApVcRSBL11ZPEqO
"""

import numpy as np
import matplotlib.pyplot as plt

cos  = np.cos 
sin  = np.sin
pi   = np.pi
sqrt = np.sqrt
acos = np.arccos

## parameters
d_star            = 3*.249e-9; 
cell_res          = 5e-6;
cell_radius       = (np.sqrt(2)/2)*cell_res;
data_num          = 10000000;
force_original_lb = -1.338688085676038e+09;
force_original_ub = +1.338688085676038e+09;

## functions 
def fun_slxx(a,r):
    slxx = -(3*sin(a)-2*sin(a)**3)/r
    return slxx


def fun_slxy(a,r):
    slxy = -(1*cos(a)-2*cos(a)**3)/r
    return slxy

def fun_slyy(a,r):
    slyy = +(1*sin(a)-2*sin(a)**3)/r
    return slyy

def fun_sgxx(a,r,t):
    sgxx = fun_slxx(a,r)*cos(t)**2+1*fun_slyy(a,r)*sin(t)**2-2*fun_slxy(a,r)*sin(t)*cos(t)
    return sgxx

def fun_sgxy(a,r,t):
    sgxy = -(fun_slyy(a,r)-fun_slxx(a,r))*sin(t)*cos(t)+(fun_slxy(a,r))*(cos(t)**2-sin(t)**2)
    return sgxy

def fun_sgyy(a,r,t):
    sgyy = 1*fun_slxx(a,r)*sin(t)**2+1*fun_slyy(a,r)*cos(t)**2+2*fun_slxy(a,r)*sin(t)*cos(t)
    return sgyy

def fun_sgxxi(a,sgxx,t):
    rlj = (sin(t)**2*(sin(a) - 2*sin(a)**3) - cos(t)**2*(3*sin(a) - 2*sin(a)**3) + 2*cos(t)*sin(t)*(cos(a) - 2*cos(a)**3))/r
    return rlj

def fun_sgxyi(a,sgxy,t):
    rlj = -((cos(t)**2 - sin(t)**2)*(cos(a) - 2*cos(a)**3) + cos(t)*sin(t)*(4*sin(a) - 4*sin(a)**3))/r
    return rlj

def fun_sgyyi(a,sgyy,t):
    rlj = -(sin(t)**2*(3*sin(a) - 2*sin(a)**3) - cos(t)**2*(sin(a) - 2*sin(a)**3) + 2*cos(t)*sin(t)*(cos(a) - 2*cos(a)**3))/r
    return rlj

def fun_ccs2pcs(x,y):
  r = sqrt(x**2 + y**2)
  a = fun_wrap2pi(np.arctan2(y,x))

  return a,r

def fun_pcs2ccs(a,r):
    x = r*cos(a)
    y = r*sin(a)
    return x,y

def fun_wrapTo2pi(x):
  xwrap = np.remainder(x, 2*pi)
  idx = np.abs(xwrap) > 2*pi
  xwrap[idx] -= 2*pi * np.sign(xwrap[idx]);
  return xwrap

def fun_glb2loc(agb,rgb,tgb,agt,rgt):
    xgt, ygt   = fun_pcs2ccs(agt,rgt)
    xgb, ygb   = fun_pcs2ccs(agb,rgb)
    xrt        = xgt - xgb
    yrt        = ygt - ygb
    xlt        = +xrt*cos(tgb) + yrt*sin(tgb) 
    ylt        = -xrt*sin(tgb) + yrt*cos(tgb)
    alt, rlt   = fun_ccs2pcs(xlt,ylt)

    return alt,rlt

def fun_scale(x,lb=0,ub=1):
    return ((x-np.min(x,axis=0))/(np.max(x,axis=0)-np.min(x,axis=0)))*(ub-lb) + lb

def fun_scaleback(x,lb,ub):
    delta_val = ub-lb
    return x*delta_val + lb

def fun_fg(a,r,g,t):
  return (cos(3*a - 2*g + 2*t) + cos(a - 2*g + 2*t))/(2*r);

def fun_fgi(a,fg,g,t):
  return (cos(3*a - 2*g + 2*t) + cos(a - 2*g + 2*t))/(2*fg);

## create random seed
np.random.seed(30)

## generate random data in local polar coordinate system
theta_original_i = np.random.rand(data_num,1)*2*np.pi
alpha_original_j = np.random.rand(data_num,1)*2*np.pi
theta_original_j = np.random.rand(data_num,1)*2*np.pi
force_original_g = fun_scale(np.random.rand(data_num,1), force_original_lb, force_original_ub);
radia_original_j = fun_fgi(alpha_original_j, force_original_g, theta_original_j, theta_original_i)

data_num         = radia_original_j.shape[0]
#print('data_num = {}'.format(data_num))

## wrap negetive radials 
alpha_original_j[radia_original_j<0] = fun_wrapTo2pi(alpha_original_j[radia_original_j<0] + np.pi)
radia_original_j[radia_original_j<0] = np.abs(radia_original_j[radia_original_j<0])

data_num         = radia_original_j.shape[0]
#print('data_num = {}'.format(data_num))

## delet the data that violate the constraints
ind_good         = radia_original_j>=d_star
theta_original_i = np.expand_dims(theta_original_i[ind_good], axis = 1)
alpha_original_j = np.expand_dims(alpha_original_j[ind_good], axis = 1)
theta_original_j = np.expand_dims(theta_original_j[ind_good], axis = 1)
radia_original_j = np.expand_dims(radia_original_j[ind_good], axis = 1)
radia_logarith_j = np.log10(radia_original_j)

data_num         = radia_original_j.shape[0]
#print('data_num = {}'.format(data_num))

## compute output of the modified data
force_ubiasedd_g = fun_fg(alpha_original_j, radia_original_j, theta_original_j, theta_original_i)

## Check out some histograms
fig, axs = plt.subplots(2, 3,figsize=(15,10))

axs[0, 0].hist(theta_original_i,100);
axs[0, 0].set_title('theta_original_i');

axs[1, 0].hist(theta_original_j,100);
axs[1, 0].set_title('theta_original_j');

axs[0, 1].hist(alpha_original_j,100);
axs[0, 1].set_title('alpha_original_j');

axs[1, 1].hist(radia_original_j ,100);
axs[1, 1].set_title('radia_original_j ');

axs[0, 2].hist(radia_logarith_j ,100);
axs[0, 2].set_title('radia_logarith_j ');

axs[1, 2].hist(force_ubiasedd_g ,100);
axs[1, 2].set_title('force_ubiasedd_g');

filename = 'force_histograms.png'
plt.savefig(filename, dpi=600)

## create datapoints and save them
# raw data
datain_raw = np.concatenate((theta_original_i, alpha_original_j, radia_original_j, theta_original_j), axis = 1)
dataou_raw = force_ubiasedd_g
dict_raw   = {'datain_raw':datain_raw,'dataou_raw':dataou_raw}

np.save('data_force_raw.npy', np.array([dict_raw]))

# scaled data
radia_logarith_lb = radia_logarith_j.min()
radia_logarith_ub = radia_logarith_j.max()
radia_scaleddd_j  = fun_scale(radia_logarith_j,0,1)

datain_scl        = np.concatenate((theta_original_i/(2*np.pi), alpha_original_j/(2*np.pi), radia_scaleddd_j, theta_original_j/(2*np.pi)), axis = 1)
dataou_scl        = force_ubiasedd_g/force_original_ub

dict_scl   = {'datain_scl':datain_scl,'dataou_scl':dataou_scl, 'radia_logarith_lb':radia_logarith_lb, 'radia_logarith_ub': radia_logarith_ub}

np.save('data_force_scl.npy', np.array([dict_scl]))

datain = np.concatenate((datain_scl,dataou_scl),axis = 1)
datain_unique = np.unique(datain,axis = 0)

if np.int(datain.shape[0]) == np.int(datain_unique.shape[0]):
  print('$ Force data repository has been created and saved in the directory | Data is unique $')
  print("$ Proceed to training-testing $")
else:
  print('$ Force data repository has been created and saved in the directory | Data is not unique $')