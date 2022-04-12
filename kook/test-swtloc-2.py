from swtloc import SWTLocalizer
from swtloc.configs import (IMAGE_ORIGINAL, 
                            IMAGE_GRAYSCALE,
                            IMAGE_EDGED,
                            IMAGE_SWT_TRANSFORMED,
                            IMAGE_CONNECTED_COMPONENTS_3C,
                            IMAGE_CONNECTED_COMPONENTS_3C_WITH_PRUNED_ELEMENTS,
                            IMAGE_CONNECTED_COMPONENTS_PRUNED_3C,
                            IMAGE_PRUNED_3C_LETTER_LOCALIZATIONS,
                            IMAGE_ORIGINAL_LETTER_LOCALIZATIONS,
                            IMAGE_ORIGINAL_MASKED_LETTER_LOCALIZATIONS,
                            IMAGE_PRUNED_3C_WORD_LOCALIZATIONS,
                            IMAGE_ORIGINAL_WORD_LOCALIZATIONS,
                            IMAGE_ORIGINAL_MASKED_WORD_LOCALIZATIONS)

def save_results(swtimgobj, res_path):
    """Helper Function"""
    savepath1 = swtimgobj.showImage(image_codes=[IMAGE_ORIGINAL, IMAGE_GRAYSCALE, IMAGE_EDGED, IMAGE_SWT_TRANSFORMED],
                                   plot_title='SWT', plot_sup_title=f'\nTransform Time - {swtImgObj.transform_time}',
                                   save_fig=True, save_dir=res_path, dpi=300)

    savepath2 = swtimgobj.showImage(image_codes=[IMAGE_CONNECTED_COMPONENTS_3C,
                                                IMAGE_CONNECTED_COMPONENTS_3C_WITH_PRUNED_ELEMENTS,
                                                IMAGE_PRUNED_3C_LETTER_LOCALIZATIONS,
                                                IMAGE_ORIGINAL_MASKED_LETTER_LOCALIZATIONS],
                                     plot_title='Letter Localizations\n',
                                   plot_sup_title=rf"Localization Method : ${swtimgobj.cfg['swtimage.localizeletters.localize_by']}$",
                                   save_fig=True, save_dir=res_path, dpi=300)

    savepath3 = swtimgobj.showImage(image_codes=[IMAGE_PRUNED_3C_WORD_LOCALIZATIONS,
                                                IMAGE_ORIGINAL_WORD_LOCALIZATIONS,
                                                 IMAGE_ORIGINAL_MASKED_WORD_LOCALIZATIONS],
                                    plot_title='Word Localizations\n',
                                    plot_sup_title=rf"Localization Method : ${swtimgobj.cfg['swtimage.localizewords.localize_by']}$",
                                    save_fig=True, save_dir=res_path, dpi=300)
    
    print('First Result Image : ', savepath1)
    print('Second Result Image : ', savepath2)
    print('Third Result Image : ', savepath3)
    
imgpath = 'issue21/issue21.jpg'
respath = 'issue21/results/'
swtl = SWTLocalizer(image_paths=imgpath)
swtImgObj = swtl.swtimages[0]

# Transformation
swt_mat = swtImgObj.transformImage(text_mode='db_lf',
                                   maximum_stroke_width=50)

letters = swtImgObj.localizeLetters()
words = swtImgObj.localizeWords()

save_results(swtimgobj=swtImgObj, res_path=respath)