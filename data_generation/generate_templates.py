# -*- coding: utf-8 -*-
import MEArec as mr


template_output_file =  './templates/templates_L5_n50.h5'

templates_params = mr.get_default_templates_params()
cell_models_folder = mr.get_default_cell_models_folder()

templates_params['n'] = 50
templates_params['drifting'] = True
templates_params['probe'] = 'tetrode-mea-l'

tempgen = mr.gen_templates(cell_models_folder = cell_models_folder, parallel = True, params = templates_params, verbose = False)
mr.save_template_generator(tempgen, template_output_file)