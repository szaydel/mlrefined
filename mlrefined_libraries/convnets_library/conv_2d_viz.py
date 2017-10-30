# import custom JS animator
from mlrefined_libraries.JSAnimation_slider_only import IPython_display_slider_only

# import standard plotting and animation
import matplotlib.pyplot as plt
plt.rc('text', usetex=True)
import matplotlib.animation as animation
from IPython.display import clear_output
import time
from matplotlib import gridspec

# import other packages
import numpy as np
import math


class visualizer:
    '''
    Illustrate convolution/cross-correlation of an input image with variable size kernels.
    '''
    def __init__(self,**args):
        self.img = args['img']                       # input image

        
    def draw_it(self,**kwargs):
        
        num_frames = 100                       
        
        if 'num_frames' in kwargs:
            num_frames = kwargs['num_frames']
            
        # initialize figure
        fig = plt.figure(figsize = (10,7))
        artist = fig
        


        # create subplot with 3 panels, plot input function in center plot
        gs = gridspec.GridSpec(1, 3, width_ratios=[1,3, 1]) 
        ax1 = plt.subplot(gs[0]); ax1.axis('off');
        ax3 = plt.subplot(gs[2]); ax3.axis('off');
        ax = plt.subplot(gs[1])

        
        # slider (horizontal axis)
        slider = np.linspace(0.001, 15, num_frames+1)
        
        print ('starting animation rendering...')
    
        
        # this subfunction padds the input image
        def myPadding_2d (img, kernel_size):
            
            # add top and bottom paddings
            L1 = kernel_size[0] 
            top = np.repeat(np.reshape(img[0,:],(1,-1)), L1-1, axis=0)
            bottom = np.repeat(np.reshape(img[-1,:],(1,-1)), L1-1, axis=0)
            img = np.concatenate((top,img),0)
            img = np.concatenate((img,bottom),0)
            
            # add left and right paddings     
            L2 = kernel_size[1]
            left = np.repeat(np.reshape(img[:,0],(-1,1)), L2-1, axis=1)
            right = np.repeat(np.reshape(img[:,-1],(-1,1)), L2-1, axis=1)
            img = np.concatenate((left,img),1)
            img = np.concatenate((img,right),1)
   
            return img

        
        # subfunction for 2d convolution/cross-correlation
        def myConvolution_2d (img, kernel):
            
            N1 = np.size(img, 0)
            N2 = np.size(img, 1)
            L1 = np.size(kernel, 0)
            L2 = np.size(kernel, 1)
    
            padded_img = myPadding_2d(img, [L1, L2])
    
            conv_img = np.zeros((N1,N2))
            for i in range(0, N1):
                for j in range(0, N2):
                    conv_img[i,j] = sum(sum(padded_img[i:i+L1, j:j+L2]*kernel))
            
            return conv_img
            
        
        
        # animation sub-function
        def animate(k):
            
            # clear the panel
            ax.cla()
            
            # print rendering update
            if np.mod(k+1,25) == 0:
                print ('rendering animation frame ' + str(k+1) + ' of ' + str(num_frames))
            if k == num_frames - 1:
                print ('animation rendering complete!')
                time.sleep(1.5)
                clear_output()
            
            # kernel size for the current frame 
            sig = slider[k]
            
            # construct the kernel 
            #kernel = np.ones((kernel_size,kernel_size))
            #kernel = kernel/sum(sum(kernel))
            kernel_size = 30
            half_size = int((kernel_size-1)/2) 
            row = np.zeros((1, kernel_size))
            for i in range(0, kernel_size):
                row[0,i] =  (1/(np.sqrt(2*np.pi)*sig))*np.exp(-(i-half_size)**2/(2*sig**2))
                
            kernel = np.dot(row.T, row) 
            kernel = kernel/sum(sum(kernel))
                

            # compute convolution/cross-correlation for the current frame
            conv_img = myConvolution_2d(self.img, kernel)

            # plot conv image
            ax.imshow(conv_img, cmap = 'gray', interpolation = 'bicubic')
                
            
            
            # plot convolution/cross-correlation
            #ax.plot(y_hat, color = 'red', linewidth=2.5)
               
            
            # fix viewing limits on panel
            #ax.set_ylim([min(self.y)-2, max(self.y)+2])

            # set tickmarks
            ax.set_xticks([])
            ax.set_yticks([])     
            
            # label axes
            #ax.set_xlabel('$\mathrm{days\,\,elapsed}$', fontsize = 12)
            #ax.set_ylabel('$\mathrm{approval\,\,ratings\,\,(\%)}$', fontsize = 12, rotation = 90, labelpad = 15)
            
            # set axis 
            #ax.axhline(y=0, color='k', zorder = 0, linewidth = 0.5)
            


            
            
            return artist,
        
        anim = animation.FuncAnimation(fig, animate,frames=num_frames, interval=num_frames, blit=True)
        
        return(anim)