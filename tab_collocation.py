#
# Wordless: Collocation
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#

import copy

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import nltk

from wordless_widgets import *
from wordless_utils import *

class Wordless_Table_Collocation(wordless_table.Wordless_Table):
    def __init__(self, main):
        super().__init__(main,
                         headers = [
                             main.tr('Rank'),
                             main.tr('Keywords'),
                             main.tr('Collocates'),
                             main.tr('Files Found'),
                         ],
                         cols_pct = [
                             main.tr('Files Found')
                         ],
                         sorting_enabled = True)

    def update_filters(self):
        if any([self.item(0, i) for i in range(self.columnCount())]):
            settings = self.main.settings_custom['collocation']

            if settings['freq_left_apply_to'] == self.tr('Total'):
                col_freq_left = self.find_col(self.tr('Total Freq/L'))
            else:
                col_freq_left = self.find_col(self.tr(f'[{settings["freq_apply_to"]}] Freq/L'))
            if settings['freq_right_apply_to'] == self.tr('Total'):
                col_freq_right = self.find_col(self.tr('Total Freq/R'))
            else:
                col_freq_right = self.find_col(self.tr(f'[{settings["freq_apply_to"]}] Freq/R'))
            if settings['score_left_apply_to'] == self.tr('Total'):
                col_score_left = self.find_col(self.tr('Total Score/L'))
            else:
                col_score_left = self.find_col(self.tr(f'[{settings["freq_apply_to"]}] Score/L'))
            if settings['score_right_apply_to'] == self.tr('Total'):
                col_score_right = self.find_col(self.tr('Total Score/R'))
            else:
                col_score_right = self.find_col(self.tr(f'[{settings["freq_apply_to"]}] Score/R'))
            col_collocates = self.find_col('Collocates')
            col_files_found = self.find_col('Files Found')

            freq_left_min = settings['freq_left_min']
            freq_left_max = settings['freq_left_max'] if not settings['freq_left_no_limit'] else float('inf')
            freq_right_min = settings['freq_right_min']
            freq_right_max = settings['freq_right_max'] if not settings['freq_right_no_limit'] else float('inf')
            score_left_min = settings['score_left_min']
            score_left_max = settings['score_left_max'] if not settings['score_left_no_limit'] else float('inf')
            score_right_min = settings['score_right_min']
            score_right_max = settings['score_right_max'] if not settings['score_right_no_limit'] else float('inf')
            len_min = settings['len_min']
            len_max = settings['len_max'] if not settings['len_no_limit'] else float('inf')
            files_min = settings['files_min']
            files_max = settings['files_max'] if not settings['files_no_limit'] else float('inf')

            self.row_filters = [{} for i in range(self.rowCount())]

            for i in range(self.rowCount()):
                if freq_left_min <= self.item(i, col_freq_left).val <= freq_left_max:
                    self.row_filters[i][self.tr('Freq/L')] = True
                else:
                    self.row_filters[i][self.tr('Freq/L')] = False
                if freq_right_min <= self.item(i, col_freq_right).val <= freq_right_max:
                    self.row_filters[i][self.tr('Freq/R')] = True
                else:
                    self.row_filters[i][self.tr('Freq/R')] = False

                if score_left_min <= self.item(i, col_score_left).val <= score_left_max:
                    self.row_filters[i][self.tr('Score/L')] = True
                else:
                    self.row_filters[i][self.tr('Score/L')] = False
                if score_right_min <= self.item(i, col_score_right).val <= score_right_max:
                    self.row_filters[i][self.tr('Score/R')] = True
                else:
                    self.row_filters[i][self.tr('Score/R')] = False

                if len_min <= len(self.item(i, col_collocates).text().replace(' ', '')) <= len_max:
                    self.row_filters[i][self.tr('Collocates')] = True
                else:
                    self.row_filters[i][self.tr('Collocates')] = False

                if files_min <= self.item(i, col_files_found).val <= files_max:
                    self.row_filters[i][self.tr('Files Found')] = True
                else:
                    self.row_filters[i][self.tr('Files Found')] = False

            self.filter_table()

def init(main):
    def load_settings(defaults = False):
        if defaults:
            settings_loaded = copy.deepcopy(main.settings_default['collocation'])
        else:
            settings_loaded = copy.deepcopy(main.settings_custom['collocation'])

        checkbox_words.setChecked(settings_loaded['words'])
        checkbox_lowercase.setChecked(settings_loaded['lowercase'])
        checkbox_uppercase.setChecked(settings_loaded['uppercase'])
        checkbox_title_case.setChecked(settings_loaded['title_case'])
        checkbox_treat_as_lowercase.setChecked(settings_loaded['treat_as_lowercase'])
        checkbox_lemmatize.setChecked(settings_loaded['lemmatize'])
        checkbox_filter_stop_words.setChecked(settings_loaded['filter_stop_words'])

        checkbox_nums.setChecked(settings_loaded['nums'])
        checkbox_puncs.setChecked(settings_loaded['puncs'])

        line_edit_search_term.setText(settings_loaded['search_term'])
        list_search_terms.clear()
        for search_term in settings_loaded['search_terms']:
            list_search_terms.add_item(search_term)

        checkbox_ignore_case.setChecked(settings_loaded['ignore_case'])
        checkbox_match_inflected_forms.setChecked(settings_loaded['match_inflected_forms'])
        checkbox_match_whole_word.setChecked(settings_loaded['match_whole_word'])
        checkbox_use_regex.setChecked(settings_loaded['use_regex'])
        checkbox_multi_search_mode.setChecked(settings_loaded['multi_search_mode'])
        checkbox_show_all.setChecked(settings_loaded['show_all'])

        checkbox_window_sync.setChecked(settings_loaded['window_sync'])
        if settings_loaded['window_left'] < 0:
            spin_box_window_left.setPrefix('L')
            spin_box_window_left.setValue(-settings_loaded['window_left'])
        else:
            spin_box_window_left.setPrefix('R')
            spin_box_window_left.setValue(settings_loaded['window_left'])
        if settings_loaded['window_right'] < 0:
            spin_box_window_right.setPrefix('L')
            spin_box_window_right.setValue(-settings_loaded['window_right'])
        else:
            spin_box_window_right.setPrefix('R')
            spin_box_window_right.setValue(settings_loaded['window_right'])
        combo_box_assoc_measure.setCurrentText(settings_loaded['assoc_measure'])

        checkbox_show_pct.setChecked(settings_loaded['show_pct'])
        checkbox_show_cumulative.setChecked(settings_loaded['show_cumulative'])
        checkbox_show_breakdown_position.setChecked(settings_loaded['show_breakdown_position'])
        checkbox_show_breakdown_file.setChecked(settings_loaded['show_breakdown_file'])

        checkbox_rank_no_limit.setChecked(settings_loaded['rank_no_limit'])
        spin_box_rank_min.setValue(settings_loaded['rank_min'])
        spin_box_rank_max.setValue(settings_loaded['rank_max'])
        checkbox_cumulative.setChecked(settings_loaded['cumulative'])

        checkbox_freq_left_no_limit.setChecked(settings_loaded['freq_left_no_limit'])
        spin_box_freq_left_min.setValue(settings_loaded['freq_left_min'])
        spin_box_freq_left_max.setValue(settings_loaded['freq_left_max'])
        combo_box_freq_left_apply_to.setCurrentText(settings_loaded['freq_left_apply_to'])
        checkbox_freq_right_no_limit.setChecked(settings_loaded['freq_right_no_limit'])
        spin_box_freq_right_min.setValue(settings_loaded['freq_right_min'])
        spin_box_freq_right_max.setValue(settings_loaded['freq_right_max'])
        combo_box_freq_right_apply_to.setCurrentText(settings_loaded['freq_right_apply_to'])

        checkbox_score_left_no_limit.setChecked(settings_loaded['score_left_no_limit'])
        spin_box_score_left_min.setValue(settings_loaded['score_left_min'])
        spin_box_score_left_max.setValue(settings_loaded['score_left_max'])
        combo_box_score_left_apply_to.setCurrentText(settings_loaded['score_left_apply_to'])
        checkbox_score_right_no_limit.setChecked(settings_loaded['score_right_no_limit'])
        spin_box_score_right_min.setValue(settings_loaded['score_right_min'])
        spin_box_score_right_max.setValue(settings_loaded['score_right_max'])
        combo_box_score_right_apply_to.setCurrentText(settings_loaded['score_right_apply_to'])

        checkbox_len_no_limit.setChecked(settings_loaded['len_no_limit'])
        spin_box_len_min.setValue(settings_loaded['len_min'])
        spin_box_len_max.setValue(settings_loaded['len_max'])

        checkbox_files_no_limit.setChecked(settings_loaded['files_no_limit'])
        spin_box_files_min.setValue(settings_loaded['files_min'])
        spin_box_files_max.setValue(settings_loaded['files_max'])

        token_settings_changed()
        search_settings_changed()
        generation_settings_changed()
        table_settings_changed()
        plot_settings_changed()
        filter_settings_changed()

    def token_settings_changed():
        settings['words'] = checkbox_words.isChecked()
        settings['lowercase'] = checkbox_lowercase.isChecked()
        settings['uppercase'] = checkbox_uppercase.isChecked()
        settings['title_case'] = checkbox_title_case.isChecked()
        settings['treat_as_lowercase'] = checkbox_treat_as_lowercase.isChecked()
        settings['lemmatize'] = checkbox_lemmatize.isChecked()
        settings['filter_stop_words'] = checkbox_filter_stop_words.isChecked()

        settings['nums'] = checkbox_nums.isChecked()
        settings['puncs'] = checkbox_puncs.isChecked()

    def search_settings_changed():
        settings['search_term'] = line_edit_search_term.text()
        settings['search_terms'] = list_search_terms.get_items()

        settings['ignore_case'] = checkbox_ignore_case.isChecked()
        settings['match_inflected_forms'] = checkbox_match_inflected_forms.isChecked()
        settings['match_whole_word'] = checkbox_match_whole_word.isChecked()
        settings['use_regex'] = checkbox_use_regex.isChecked()
        settings['multi_search_mode'] = checkbox_multi_search_mode.isChecked()
        settings['show_all'] = checkbox_show_all.isChecked()

        if main.settings_custom['collocation']['show_all']:
            table_collocation.button_generate_data.setText(main.tr('Generate Collocates'))
        else:
            table_collocation.button_generate_data.setText(main.tr('Search Collocates'))

    def generation_settings_changed():
        settings['window_sync'] = checkbox_window_sync.isChecked()
        if spin_box_window_left.prefix() == 'L':
            settings['window_left'] = -spin_box_window_left.value()
        else:
            settings['window_left'] = spin_box_window_left.value()
        if spin_box_window_right.prefix() == 'L':
            settings['window_right'] = -spin_box_window_right.value()
        else:
            settings['window_right'] = spin_box_window_right.value()
        settings['assoc_measure'] = combo_box_assoc_measure.currentText()

    def table_settings_changed():
        settings['show_pct'] = checkbox_show_pct.isChecked()
        settings['show_cumulative'] = checkbox_show_cumulative.isChecked()
        settings['show_breakdown_position'] = checkbox_show_breakdown_position.isChecked()
        settings['show_breakdown_file'] = checkbox_show_breakdown_file.isChecked()

    def plot_settings_changed():
        settings['rank_no_limit'] = checkbox_rank_no_limit.isChecked()
        settings['rank_min'] = spin_box_rank_min.value()
        settings['rank_max'] = spin_box_rank_max.value()

        settings['cumulative'] = checkbox_cumulative.isChecked()

    def filter_settings_changed():
        settings['freq_left_no_limit'] = checkbox_freq_left_no_limit.isChecked()
        settings['freq_left_min'] = spin_box_freq_left_min.value()
        settings['freq_left_max'] = spin_box_freq_left_max.value()
        settings['freq_left_apply_to'] = combo_box_freq_left_apply_to.currentText()
        settings['freq_right_no_limit'] = checkbox_freq_right_no_limit.isChecked()
        settings['freq_right_min'] = spin_box_freq_right_min.value()
        settings['freq_right_max'] = spin_box_freq_right_max.value()
        settings['freq_right_apply_to'] = combo_box_freq_right_apply_to.currentText()

        settings['score_left_no_limit'] = checkbox_score_left_no_limit.isChecked()
        settings['score_left_min'] = spin_box_score_left_min.value()
        settings['score_left_max'] = spin_box_score_left_max.value()
        settings['score_left_apply_to'] = combo_box_score_left_apply_to.currentText()
        settings['score_right_no_limit'] = checkbox_score_right_no_limit.isChecked()
        settings['score_right_min'] = spin_box_score_right_min.value()
        settings['score_right_max'] = spin_box_score_right_max.value()
        settings['score_right_apply_to'] = combo_box_score_right_apply_to.currentText()

        settings['len_no_limit'] = checkbox_len_no_limit.isChecked()
        settings['len_min'] = spin_box_len_min.value()
        settings['len_max'] = spin_box_len_max.value()

        settings['files_no_limit'] = checkbox_files_no_limit.isChecked()
        settings['files_min'] = spin_box_files_min.value()
        settings['files_max'] = spin_box_files_max.value()

        table_collocation.update_filters()

    settings = main.settings_custom['collocation']

    tab_collocation = wordless_layout.Wordless_Tab(main, load_settings)
    
    table_collocation = Wordless_Table_Collocation(main)

    table_collocation.button_generate_data = QPushButton(main.tr('Generate Collocates'), main)
    table_collocation.button_generate_plot = QPushButton(main.tr('Generate Plot'), main)

    table_collocation.button_generate_data.clicked.connect(lambda: generate_data(main, table_collocation))
    table_collocation.button_generate_plot.clicked.connect(lambda: generate_plot(main))

    tab_collocation.layout_table.addWidget(table_collocation, 0, 0, 1, 5)
    tab_collocation.layout_table.addWidget(table_collocation.button_generate_data, 1, 0)
    tab_collocation.layout_table.addWidget(table_collocation.button_generate_plot, 1, 1)
    tab_collocation.layout_table.addWidget(table_collocation.button_export_selected, 1, 2)
    tab_collocation.layout_table.addWidget(table_collocation.button_export_all, 1, 3)
    tab_collocation.layout_table.addWidget(table_collocation.button_clear, 1, 4)

    # Token Settings
    group_box_token_settings = QGroupBox(main.tr('Token Settings'), main)

    (checkbox_words,
     checkbox_lowercase,
     checkbox_uppercase,
     checkbox_title_case,
     checkbox_treat_as_lowercase,
     checkbox_lemmatize,
     checkbox_filter_stop_words,

     checkbox_nums,
     checkbox_puncs) = wordless_widgets.wordless_widgets_token(main)

    separator_token_settings = wordless_layout.Wordless_Separator(main)

    checkbox_words.stateChanged.connect(token_settings_changed)
    checkbox_lowercase.stateChanged.connect(token_settings_changed)
    checkbox_uppercase.stateChanged.connect(token_settings_changed)
    checkbox_title_case.stateChanged.connect(token_settings_changed)
    checkbox_treat_as_lowercase.stateChanged.connect(token_settings_changed)
    checkbox_lemmatize.stateChanged.connect(token_settings_changed)
    checkbox_filter_stop_words.stateChanged.connect(token_settings_changed)

    checkbox_nums.stateChanged.connect(token_settings_changed)
    checkbox_puncs.stateChanged.connect(token_settings_changed)

    group_box_token_settings.setLayout(QGridLayout())
    group_box_token_settings.layout().addWidget(checkbox_words, 0, 0)
    group_box_token_settings.layout().addWidget(checkbox_lowercase, 0, 1)
    group_box_token_settings.layout().addWidget(checkbox_uppercase, 1, 0)
    group_box_token_settings.layout().addWidget(checkbox_title_case, 1, 1)
    group_box_token_settings.layout().addWidget(checkbox_treat_as_lowercase, 2, 0, 1, 2)
    group_box_token_settings.layout().addWidget(checkbox_lemmatize, 3, 0, 1, 2)
    group_box_token_settings.layout().addWidget(checkbox_filter_stop_words, 4, 0, 1, 2)

    group_box_token_settings.layout().addWidget(separator_token_settings, 5, 0, 1, 2)

    group_box_token_settings.layout().addWidget(checkbox_nums, 6, 0)
    group_box_token_settings.layout().addWidget(checkbox_puncs, 6, 1)

    # Search Settings
    group_box_search_settings = QGroupBox(main.tr('Search Settings'), main)

    (label_search_term,
     checkbox_show_all,
     line_edit_search_term,
     list_search_terms,
     checkbox_ignore_case,
     checkbox_match_inflected_forms,
     checkbox_match_whole_word,
     checkbox_use_regex,
     checkbox_multi_search_mode) = wordless_widgets.wordless_widgets_search(main)

    line_edit_search_term.textChanged.connect(search_settings_changed)
    line_edit_search_term.returnPressed.connect(table_collocation.button_generate_data.click)
    list_search_terms.itemChanged.connect(search_settings_changed)

    checkbox_ignore_case.stateChanged.connect(search_settings_changed)
    checkbox_match_inflected_forms.stateChanged.connect(search_settings_changed)
    checkbox_match_whole_word.stateChanged.connect(search_settings_changed)
    checkbox_use_regex.stateChanged.connect(search_settings_changed)
    checkbox_multi_search_mode.stateChanged.connect(search_settings_changed)
    checkbox_show_all.stateChanged.connect(search_settings_changed)

    layout_show_all = QGridLayout()
    layout_show_all.addWidget(label_search_term, 0, 0, Qt.AlignLeft)
    layout_show_all.addWidget(checkbox_show_all, 0, 1, Qt.AlignRight)

    layout_search_terms = QGridLayout()
    layout_search_terms.addWidget(list_search_terms, 0, 0, 6, 1)
    layout_search_terms.addWidget(list_search_terms.button_add, 0, 1)
    layout_search_terms.addWidget(list_search_terms.button_insert, 1, 1)
    layout_search_terms.addWidget(list_search_terms.button_remove, 2, 1)
    layout_search_terms.addWidget(list_search_terms.button_clear, 3, 1)
    layout_search_terms.addWidget(list_search_terms.button_import, 4, 1)
    layout_search_terms.addWidget(list_search_terms.button_export, 5, 1)

    group_box_search_settings.setLayout(QGridLayout())
    group_box_search_settings.layout().addLayout(layout_show_all, 0, 0, 1, 4)
    group_box_search_settings.layout().addWidget(line_edit_search_term, 1, 0, 1, 4)
    group_box_search_settings.layout().addLayout(layout_search_terms, 2, 0, 1, 4)

    group_box_search_settings.layout().addWidget(checkbox_ignore_case, 3, 0, 1, 4)
    group_box_search_settings.layout().addWidget(checkbox_match_inflected_forms, 4, 0, 1, 4)
    group_box_search_settings.layout().addWidget(checkbox_match_whole_word, 5, 0, 1, 4)
    group_box_search_settings.layout().addWidget(checkbox_use_regex, 6, 0, 1, 4)
    group_box_search_settings.layout().addWidget(checkbox_multi_search_mode, 7, 0, 1, 4)

    # Generation Settings
    group_box_generation_settings = QGroupBox(main.tr('Generation Settings'))

    label_window = QLabel(main.tr('Collocational Window:'), main)
    (checkbox_window_sync,
     label_window_left,
     spin_box_window_left,
     label_window_right,
     spin_box_window_right) = wordless_widgets.wordless_widgets_window(main)

    label_assoc_measure = QLabel(main.tr('Association Measure:'), main)
    combo_box_assoc_measure = QComboBox(main)

    combo_box_assoc_measure.addItems(main.settings_global['assoc_measures'])

    checkbox_window_sync.stateChanged.connect(generation_settings_changed)
    spin_box_window_left.valueChanged.connect(generation_settings_changed)
    spin_box_window_right.valueChanged.connect(generation_settings_changed)
    combo_box_assoc_measure.currentTextChanged.connect(generation_settings_changed)

    group_box_generation_settings.setLayout(QGridLayout())
    group_box_generation_settings.layout().addWidget(label_window, 0, 0, 1, 3)
    group_box_generation_settings.layout().addWidget(checkbox_window_sync, 0, 3)
    group_box_generation_settings.layout().addWidget(label_window_left, 1, 0)
    group_box_generation_settings.layout().addWidget(spin_box_window_left, 1, 1)
    group_box_generation_settings.layout().addWidget(label_window_right, 1, 2)
    group_box_generation_settings.layout().addWidget(spin_box_window_right, 1, 3)
    group_box_generation_settings.layout().addWidget(label_assoc_measure, 2, 0, 1, 4)
    group_box_generation_settings.layout().addWidget(combo_box_assoc_measure, 3, 0, 1, 4)

    # Table Settings
    group_box_table_settings = QGroupBox(main.tr('Table Settings'))

    (checkbox_show_pct,
     checkbox_show_cumulative,
     checkbox_show_breakdown_file) = wordless_widgets.wordless_widgets_table(main, table_collocation)

    checkbox_show_breakdown_file.setText('Show Breakdown by File')
    checkbox_show_breakdown_position = QCheckBox('Show Breakdown by Span Position', main)

    checkbox_show_pct.stateChanged.connect(table_settings_changed)
    checkbox_show_cumulative.stateChanged.connect(table_settings_changed)
    checkbox_show_breakdown_position.stateChanged.connect(table_settings_changed)
    checkbox_show_breakdown_file.stateChanged.connect(table_settings_changed)

    group_box_table_settings.setLayout(QGridLayout())
    group_box_table_settings.layout().addWidget(checkbox_show_pct, 0, 0)
    group_box_table_settings.layout().addWidget(checkbox_show_cumulative, 1, 0)
    group_box_table_settings.layout().addWidget(checkbox_show_breakdown_position, 2, 0)
    group_box_table_settings.layout().addWidget(checkbox_show_breakdown_file, 3, 0)

    # Plot Settings
    group_box_plot_settings = QGroupBox(main.tr('Plot Settings'), main)

    label_rank = QLabel(main.tr('Rank:'), main)
    (checkbox_rank_no_limit,
     label_rank_min,
     spin_box_rank_min,
     label_rank_max,
     spin_box_rank_max) = wordless_widgets.wordless_widgets_filter(main, 1, 10000)
    checkbox_cumulative = QCheckBox(main.tr('Cumulative'), main)

    checkbox_rank_no_limit.stateChanged.connect(plot_settings_changed)
    spin_box_rank_min.valueChanged.connect(plot_settings_changed)
    spin_box_rank_max.valueChanged.connect(plot_settings_changed)
    checkbox_cumulative.stateChanged.connect(plot_settings_changed)

    group_box_plot_settings.setLayout(QGridLayout())
    group_box_plot_settings.layout().addWidget(label_rank, 0, 0, 1, 3)
    group_box_plot_settings.layout().addWidget(checkbox_rank_no_limit, 0, 3)
    group_box_plot_settings.layout().addWidget(label_rank_min, 1, 0)
    group_box_plot_settings.layout().addWidget(spin_box_rank_min, 1, 1)
    group_box_plot_settings.layout().addWidget(label_rank_max, 1, 2)
    group_box_plot_settings.layout().addWidget(spin_box_rank_max, 1, 3)
    group_box_plot_settings.layout().addWidget(checkbox_cumulative, 2, 0, 1, 4)

    # Filter Settings
    group_box_filter_settings = QGroupBox(main.tr('Filter Settings'), main)

    label_freq_left = QLabel(main.tr('Frequency (Left):'), main)
    (checkbox_freq_left_no_limit,
     label_freq_left_min,
     spin_box_freq_left_min,
     label_freq_left_max,
     spin_box_freq_left_max,
     label_freq_left_apply_to,
     combo_box_freq_left_apply_to) = wordless_widgets.wordless_widgets_filter(main,
                                                                               filter_min = 0,
                                                                               filter_max = 10000,
                                                                               table = table_collocation,
                                                                               col = main.tr('Freq/L'),
                                                                               apply_to = True)

    label_freq_right = QLabel(main.tr('Frequency (Right):'), main)
    (checkbox_freq_right_no_limit,
     label_freq_right_min,
     spin_box_freq_right_min,
     label_freq_right_max,
     spin_box_freq_right_max,
     label_freq_right_apply_to,
     combo_box_freq_right_apply_to) = wordless_widgets.wordless_widgets_filter(main,
                                                                                filter_min = 0,
                                                                                filter_max = 10000,
                                                                                table = table_collocation,
                                                                                col = main.tr('Freq/R'),
                                                                                apply_to = True)

    label_score_left = QLabel(main.tr('Score (Left):'), main)
    (checkbox_score_left_no_limit,
     label_score_left_min,
     spin_box_score_left_min,
     label_score_left_max,
     spin_box_score_left_max,
     label_score_left_apply_to,
     combo_box_score_left_apply_to) = wordless_widgets.wordless_widgets_filter(main,
                                                                               filter_min = 0,
                                                                               filter_max = 10000,
                                                                               table = table_collocation,
                                                                               col = main.tr('Score/L'),
                                                                               apply_to = True)

    label_score_right = QLabel(main.tr('Score (Right):'), main)
    (checkbox_score_right_no_limit,
     label_score_right_min,
     spin_box_score_right_min,
     label_score_right_max,
     spin_box_score_right_max,
     label_score_right_apply_to,
     combo_box_score_right_apply_to) = wordless_widgets.wordless_widgets_filter(main,
                                                                                filter_min = 0,
                                                                                filter_max = 10000,
                                                                                table = table_collocation,
                                                                                col = main.tr('Score/R'),
                                                                                apply_to = True)

    label_len = QLabel(main.tr('N-gram Length:'), main)
    (checkbox_len_no_limit,
     label_len_min,
     spin_box_len_min,
     label_len_max,
     spin_box_len_max) = wordless_widgets.wordless_widgets_filter(main,
                                                                  table = table_collocation,
                                                                  col = main.tr('Collocates'))

    label_files = QLabel(main.tr('Files Found:'), main)
    (checkbox_files_no_limit,
     label_files_min,
     spin_box_files_min,
     label_files_max,
     spin_box_files_max) = wordless_widgets.wordless_widgets_filter(main,
                                                                    filter_min = 1,
                                                                    filter_max = 1000,
                                                                    table = table_collocation,
                                                                    col = main.tr('Files Found'))

    spin_box_freq_left_min.editingFinished.connect(filter_settings_changed)
    spin_box_freq_left_max.editingFinished.connect(filter_settings_changed)
    combo_box_freq_left_apply_to.currentTextChanged.connect(filter_settings_changed)
    checkbox_freq_right_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_freq_right_min.editingFinished.connect(filter_settings_changed)
    spin_box_freq_right_max.editingFinished.connect(filter_settings_changed)
    combo_box_freq_right_apply_to.currentTextChanged.connect(filter_settings_changed)

    checkbox_score_left_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_score_left_min.editingFinished.connect(filter_settings_changed)
    spin_box_score_left_max.editingFinished.connect(filter_settings_changed)
    combo_box_score_left_apply_to.currentTextChanged.connect(filter_settings_changed)
    checkbox_score_right_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_score_right_min.editingFinished.connect(filter_settings_changed)
    spin_box_score_right_max.editingFinished.connect(filter_settings_changed)
    combo_box_score_right_apply_to.currentTextChanged.connect(filter_settings_changed)

    checkbox_len_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_len_min.editingFinished.connect(filter_settings_changed)
    spin_box_len_max.editingFinished.connect(filter_settings_changed)

    checkbox_files_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_files_min.editingFinished.connect(filter_settings_changed)
    spin_box_files_max.editingFinished.connect(filter_settings_changed)

    group_box_filter_settings.setLayout(QGridLayout())
    group_box_filter_settings.layout().addWidget(label_freq_left, 0, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(checkbox_freq_left_no_limit, 0, 3)
    group_box_filter_settings.layout().addWidget(label_freq_left_min, 1, 0)
    group_box_filter_settings.layout().addWidget(spin_box_freq_left_min, 1, 1)
    group_box_filter_settings.layout().addWidget(label_freq_left_max, 1, 2)
    group_box_filter_settings.layout().addWidget(spin_box_freq_left_max, 1, 3)
    group_box_filter_settings.layout().addWidget(label_freq_left_apply_to, 2, 0)
    group_box_filter_settings.layout().addWidget(combo_box_freq_left_apply_to, 2, 1, 1, 3)

    group_box_filter_settings.layout().addWidget(label_freq_right, 3, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(checkbox_freq_right_no_limit, 3, 3)
    group_box_filter_settings.layout().addWidget(label_freq_right_min, 4, 0)
    group_box_filter_settings.layout().addWidget(spin_box_freq_right_min, 4, 1)
    group_box_filter_settings.layout().addWidget(label_freq_right_max, 4, 2)
    group_box_filter_settings.layout().addWidget(spin_box_freq_right_max, 4, 3)
    group_box_filter_settings.layout().addWidget(label_freq_right_apply_to, 5, 0)
    group_box_filter_settings.layout().addWidget(combo_box_freq_right_apply_to, 5, 1, 1, 3)

    group_box_filter_settings.layout().addWidget(label_score_left, 6, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(checkbox_score_left_no_limit, 6, 3)
    group_box_filter_settings.layout().addWidget(label_score_left_min, 7, 0)
    group_box_filter_settings.layout().addWidget(spin_box_score_left_min, 7, 1)
    group_box_filter_settings.layout().addWidget(label_score_left_max, 7, 2)
    group_box_filter_settings.layout().addWidget(spin_box_score_left_max, 7, 3)
    group_box_filter_settings.layout().addWidget(label_score_left_apply_to, 8, 0)
    group_box_filter_settings.layout().addWidget(combo_box_score_left_apply_to, 8, 1, 1, 3)

    group_box_filter_settings.layout().addWidget(label_score_right, 9, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(checkbox_score_right_no_limit, 9, 3)
    group_box_filter_settings.layout().addWidget(label_score_right_min, 10, 0)
    group_box_filter_settings.layout().addWidget(spin_box_score_right_min, 10, 1)
    group_box_filter_settings.layout().addWidget(label_score_right_max, 10, 2)
    group_box_filter_settings.layout().addWidget(spin_box_score_right_max, 10, 3)
    group_box_filter_settings.layout().addWidget(label_score_right_apply_to, 11, 0)
    group_box_filter_settings.layout().addWidget(combo_box_score_right_apply_to, 11, 1, 1, 3)

    group_box_filter_settings.layout().addWidget(label_len, 12, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(checkbox_len_no_limit, 12, 3)
    group_box_filter_settings.layout().addWidget(label_len_min, 13, 0)
    group_box_filter_settings.layout().addWidget(spin_box_len_min, 13, 1)
    group_box_filter_settings.layout().addWidget(label_len_max, 13, 2)
    group_box_filter_settings.layout().addWidget(spin_box_len_max, 13, 3)

    group_box_filter_settings.layout().addWidget(label_files, 14, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(checkbox_files_no_limit, 14, 3)
    group_box_filter_settings.layout().addWidget(label_files_min, 15, 0)
    group_box_filter_settings.layout().addWidget(spin_box_files_min, 15, 1)
    group_box_filter_settings.layout().addWidget(label_files_max, 15, 2)
    group_box_filter_settings.layout().addWidget(spin_box_files_max, 15, 3)

    tab_collocation.layout_settings.addWidget(group_box_token_settings, 0, 0, Qt.AlignTop)
    tab_collocation.layout_settings.addWidget(group_box_search_settings, 1, 0, Qt.AlignTop)
    tab_collocation.layout_settings.addWidget(group_box_generation_settings, 2, 0, Qt.AlignTop)
    tab_collocation.layout_settings.addWidget(group_box_table_settings, 3, 0, Qt.AlignTop)
    tab_collocation.layout_settings.addWidget(group_box_plot_settings, 4, 0, Qt.AlignTop)
    tab_collocation.layout_settings.addWidget(group_box_filter_settings, 5, 0, Qt.AlignTop)

    load_settings()

    return tab_collocation

def generate_collocates(main, text):
    freq_distribution = {}
    score_distribution = {}

    settings = main.settings_custom['collocation']
    tokens = text.tokens.copy()

    if settings['window_left'] < 0 and settings['window_right'] > 0:
        window_size_left = abs(settings['window_left'])
        window_size_right = abs(settings['window_right'])
    elif settings['window_left'] > 0 and settings['window_right'] > 0:
        window_size_left = 0
        window_size_right = settings['window_right'] - settings['window_left'] + 1
    elif settings['window_left'] < 0 and settings['window_right'] < 0:
        window_size_left = settings['window_right'] - settings['window_left'] + 1
        window_size_right = 0
    window_size = window_size_left + window_size_right

    if settings['words']:
        if settings['treat_as_lowercase']:
            tokens = [token.lower() for token in tokens]

        if settings['lemmatize']:
            tokens = wordless_lemmatize(main, tokens, text.lang)

    if not settings['puncs']:
        tokens = [token for token in tokens if token.isalnum()]

    # Frequency distribution
    for ngram in nltk.ngrams(tokens, abs(settings['window_right']) + 1, pad_right = True):
        w1 = ngram[0]

        for i, w2 in enumerate(ngram[1:]):
            if w2 is not None:
                if (w1, w2) not in freq_distribution:
                    freq_distribution[(w1, w2)] = [0] * window_size

                freq_distribution[(w1, w2)][window_size_left + i] += 1

    for ngram in nltk.ngrams(tokens, abs(settings['window_left']) + 1, pad_right = True):
        w1 = ngram[0]

        for i, w2 in enumerate(ngram[1:]):
            if w2 is not None:
                if (w2, w1) not in freq_distribution:
                    freq_distribution[(w2, w1)] = [0] * window_size

                freq_distribution[(w2, w1)][-window_size_right + i] += 1

    finder_left = nltk.collocations.BigramCollocationFinder.from_words(tokens, window_size = abs(settings['window_left']) + 1)
    finder_right = nltk.collocations.BigramCollocationFinder.from_words(tokens, window_size = abs(settings['window_right']) + 1)
    assoc_measure = main.settings_global['assoc_measures'][settings['assoc_measure']]

    for collocate, score in finder_right.score_ngrams(assoc_measure):
        if collocate not in score_distribution:
            score_distribution[collocate] = [0, 0]

        score_distribution[collocate][1] = score

    for collocate, score in finder_left.score_ngrams(assoc_measure):
        collocate_reversed = tuple(reversed(collocate))

        if collocate_reversed not in score_distribution:
            score_distribution[collocate_reversed] = [0, 0]

        score_distribution[collocate_reversed][0] = score

    if not settings['show_all']:
        if settings['multi_search_mode']:
            search_terms = settings['search_terms']
        else:
            if settings['search_term']:
                search_terms = [settings['search_term']]
            else:
                search_terms = []

        search_terms = text.match_tokens(search_terms,
                                         settings['ignore_case'],
                                         settings['match_inflected_forms'],
                                         settings['match_whole_word'],
                                         settings['use_regex'])

        freq_distribution = {collocate: freqs
                             for collocate, freqs in freq_distribution.items()
                             for search_term in search_terms
                             if search_term == collocate[0]}

        score_distribution = {collocate: scores
                              for collocate, scores in score_distribution.items()
                              for search_term in search_terms
                              if search_term == collocate[0]}

    return freq_distribution, score_distribution

def generate_data(main, table):
    freq_distributions = []
    score_distributions = []

    settings = main.settings_custom['collocation']
    files = main.wordless_files.selected_files()

    if files:
        if (settings['show_all'] or
            not settings['show_all'] and (settings['multi_search_mode'] and settings['search_terms'] or
                                          not settings['multi_search_mode'] and settings['search_term'])):
            table.files = files

            window_left = True if settings['window_left'] < 0 else False
            window_right = True if settings['window_right'] > 0 else False

            if settings['window_left'] < 0 and settings['window_right'] > 0:
                window_size_left = abs(settings['window_left'])
                window_size_right = abs(settings['window_right'])
            elif settings['window_left'] > 0 and settings['window_right'] > 0:
                window_size_left = 0
                window_size_right = settings['window_right'] - settings['window_left'] + 1
            elif settings['window_left'] < 0 and settings['window_right'] < 0:
                window_size_left = settings['window_right'] - settings['window_left'] + 1
                window_size_right = 0
            window_size = window_size_left + window_size_right

            for i, file in enumerate(files):
                freq_distribution, score_distribution = generate_collocates(main, wordless_text.Wordless_Text(main, file))

                freq_distributions.append(freq_distribution)
                score_distributions.append(score_distribution)

            freq_distribution = wordless_misc.merge_dicts(freq_distributions)
            score_distribution = wordless_misc.merge_dicts(score_distributions)

            if freq_distribution:
                table.clear_table()

                # Insert columns
                for i, file in enumerate(files):
                    for i in range(settings['window_left'], settings['window_right'] + 1):
                        if i < 0:
                            table.insert_col(table.columnCount() - 1,
                                             main.tr(f'[{file["name"]}] Freq/L{-i}'),
                                             pct = True, cumulative = True, breakdown = True)
                        elif i > 0:
                            table.insert_col(table.columnCount() - 1,
                                             main.tr(f'[{file["name"]}] Freq/R{i}'),
                                             pct = True, cumulative = True, breakdown = True)

                    if window_left:
                        table.insert_col(table.columnCount() - 1,
                                         main.tr(f'[{file["name"]}] Freq/L'),
                                         pct = True, cumulative = True, breakdown = True)
                    if window_right:
                        table.insert_col(table.columnCount() - 1,
                                         main.tr(f'[{file["name"]}] Freq/R'),
                                         pct = True, cumulative = True, breakdown = True)
                    if window_left:
                        table.insert_col(table.columnCount() - 1,
                                         main.tr(f'[{file["name"]}] Score/L'),
                                         breakdown = True)
                    if window_right:
                        table.insert_col(table.columnCount() - 1,
                                         main.tr(f'[{file["name"]}] Score/R'),
                                         breakdown = True)

                for i in range(settings['window_left'], settings['window_right'] + 1):
                    if i < 0:
                        table.insert_col(table.columnCount() - 1,
                                         main.tr(f'Total Freq/L{-i}'),
                                         pct = True, cumulative = True)
                    elif i > 0:
                        table.insert_col(table.columnCount() - 1,
                                         main.tr(f'Total Freq/R{i}'),
                                         pct = True, cumulative = True)

                if window_left:
                    table.insert_col(table.columnCount() - 1,
                                     main.tr(f'Total Freq/L'),
                                     pct = True, cumulative = True)
                if window_right:
                    table.insert_col(table.columnCount() - 1,
                                     main.tr(f'Total Freq/R'),
                                     pct = True, cumulative = True)
                if window_left:
                    table.insert_col(table.columnCount() - 1, main.tr(f'Total Score/L'))
                if window_right:
                    table.insert_col(table.columnCount() - 1, main.tr(f'Total Score/R'))

                table.sortByColumn(table.find_col(main.tr(f'[{files[0]["name"]}] Score/R')), Qt.DescendingOrder)

                cols_freq = table.find_col([main.tr(f'[{file["name"]}]') for file in files], fuzzy_matching = True)
                cols_freq_left = table.find_col([main.tr(f'[{file["name"]}] Freq/L') for file in files])
                cols_freq_right = table.find_col([main.tr(f'[{file["name"]}] Freq/R') for file in files])
                cols_score_left = table.find_col([main.tr(f'[{file["name"]}] Score/L') for file in files])
                cols_score_right = table.find_col([main.tr(f'[{file["name"]}] Score/R') for file in files])
                cols_freq_total = table.find_cols(main.tr('Total'))
                col_total_freq_left = table.find_col(main.tr('Total Freq/L'))
                col_total_freq_right = table.find_col(main.tr('Total Freq/R'))
                col_total_score_left = table.find_col(main.tr('Total Score/L'))
                col_total_score_right = table.find_col(main.tr('Total Score/R'))
                col_files_found = table.find_col(main.tr('Files Found'))

                total_freqs_positions = [[sum(freqs_position) for freqs_position in zip(*freqs)] for freqs in zip(*freq_distribution.values())]
                total_freqs = [sum(total_freqs) for total_freqs in zip(*total_freqs_positions)]
                total_freq_left = sum(total_freqs[:window_size_left])
                total_freq_right = sum(total_freqs[window_size_right:])
                total_freq = total_freq_left + total_freq_right

                score_left_max = max([sum(list(zip(*scores))[0]) for scores in score_distribution.values()])
                score_right_max = max([sum(list(zip(*scores))[1]) for scores in score_distribution.values()])
                len_files = len(files)

                table.blockSignals(True)
                table.setSortingEnabled(False)
                table.setUpdatesEnabled(False)

                table.setRowCount(len(freq_distribution))

                for i, (collocate, scores) in enumerate(sorted(score_distribution.items(), key = wordless_misc.multi_sorting)):
                    # Score
                    for j, (score_left, score_right) in enumerate(scores):
                        if window_left:
                            table.set_item_num(i, cols_score_left[j], score_left, score_left_max)
                        if window_right:
                            table.set_item_num(i, cols_score_right[j], score_right, score_right_max)

                for i, ((keyword, collocate), freqs) in enumerate(sorted(freq_distribution.items(), key = wordless_misc.multi_sorting)):
                    total_freq_positions = [sum(freqs_position) for freqs_position in zip(*freqs)]

                    # Keywords
                    table.setItem(i, 1, wordless_table.Wordless_Table_Item(keyword))
                    # Collocates
                    table.setItem(i, 2, wordless_table.Wordless_Table_Item(collocate))

                    # Frequency
                    for j, freq_positions in enumerate(freqs):
                        for k, freq_position in enumerate(freq_positions):
                            table.set_item_pct(i, cols_freq[j] + k, freq_position, total_freqs_positions[j][k])

                        if window_left:
                            table.set_item_pct(i, cols_freq_left[j],
                                               sum(freq_positions[:window_size_left]),
                                               sum(total_freqs_positions[j][:window_size_left]))
                        if window_right:
                            table.set_item_pct(i, cols_freq_right[j],
                                               sum(freq_positions[-window_size_right:]),
                                               sum(total_freqs_positions[j][-window_size_right:]))

                    # Total Frequency
                    for j, total_freq in enumerate(total_freq_positions):
                        table.set_item_pct(i, cols_freq_total[j], total_freq, total_freqs[j])

                    if window_left:
                        table.set_item_pct(i, col_total_freq_left,
                                           sum(total_freq_positions[:window_size_left]),
                                           total_freq_left)
                    if window_right:
                        table.set_item_pct(i, col_total_freq_right,
                                           sum(total_freq_positions[window_size_right:]),
                                           total_freq_right)

                    # Files Found
                    table.set_item_pct(i, col_files_found,
                                       len([freqs_position for freqs_position in freqs if any(freqs_position)]), len_files)

                table.update_items_pct()
                
                table.blockSignals(False)
                table.setSortingEnabled(True)
                table.setUpdatesEnabled(True)

                #table.update_filters()
            else:
                wordless_message.empty_results_table(main)

            main.status_bar.showMessage(main.tr('Done!'))
        else:
            wordless_message.empty_search_term(main)
