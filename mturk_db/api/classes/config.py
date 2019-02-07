from django.conf import settings

class Manager_Config(object):
    @staticmethod
    def get_config():
        config = {
            'version_api': settings.VERSION_API,
            'paths': Manager_Config.get_paths(),
        }
        return config

    @staticmethod
    def get_paths():
        dictionary_paths = {
            'url_api_projects': 'projects',
            'url_api_projects_check_uniqueness': 'info_projects/uniqueness',
            'url_api_projects_balance': 'projects/{}/balance'.format(settings.PLACEHOLDER_SLUG_PROJECT),
            'url_api_projects_settings_batch': 'projects/{}/settings_batch'.format(settings.PLACEHOLDER_SLUG_PROJECT),
            'url_api_projects_templates_worker': 'projects/{}/templates_worker'.format(settings.PLACEHOLDER_SLUG_PROJECT),
            'url_api_projects_templates_assignment': 'projects/{}/templates_assignment'.format(settings.PLACEHOLDER_SLUG_PROJECT),
            'url_api_projects_templates_hit': 'projects/{}/templates_hit'.format(settings.PLACEHOLDER_SLUG_PROJECT),
            'url_api_projects_templates_global': 'projects/{}/templates_global'.format(settings.PLACEHOLDER_SLUG_PROJECT),
            'url_api_projects_batches': 'projects/{}/batches'.format(settings.PLACEHOLDER_SLUG_PROJECT),
            'url_api_projects_batches_download': 'projects/{}/download_batches'.format(settings.PLACEHOLDER_SLUG_PROJECT),
            'url_api_projects_batches_download_info': 'projects/{}/download_info_batches'.format(settings.PLACEHOLDER_SLUG_PROJECT),
            'url_api_projects_hits': 'projects/{}/hits'.format(settings.PLACEHOLDER_SLUG_PROJECT),
            'url_api_projects_assignments': 'projects/{}/assignments'.format(settings.PLACEHOLDER_SLUG_PROJECT),
            'url_api_projects_clear_sandbox': 'projects/{}/clear_sandbox'.format(settings.PLACEHOLDER_SLUG_PROJECT),
            'url_api_ping': 'projects/{}/ping'.format(settings.PLACEHOLDER_SLUG_PROJECT),

            'url_api_workers': 'projects/{}/workers'.format(settings.PLACEHOLDER_SLUG_PROJECT),
            'url_api_workers_get_blocks_hard': 'projects/{}/workers/blocks_hard'.format(settings.PLACEHOLDER_SLUG_PROJECT),

            'url_api_keywords': 'api/keywords'.format(settings.PLACEHOLDER_SLUG_PROJECT),
            'url_api_messages_reject': 'api/messages_reject'.format(settings.PLACEHOLDER_SLUG_PROJECT),
        }

        return dictionary_paths