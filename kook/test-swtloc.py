# import swtloc as swt
# imgpath = 'test-data/test.jpg'
# swtl = swt.SWTLocalizer(image_paths=imgpath)
# swtImgObj = swtl.swtimages[0]
# swt_mat = swtImgObj.transformImage(text_mode='lb_df',
#                                    auto_canny_sigma=1.0,
#                                    maximum_stroke_width=20)


import swtloc as swt
imgpath = 'test-data/test.jpg'
swtl = swt.SWTLocalizer(image_paths=imgpath)
swtImgObj = swtl.swtimages[0]
swt_mat = swtImgObj.transformImage(text_mode='db_lf',
                                   engine='python',
                                   maximum_stroke_width=20)
                                