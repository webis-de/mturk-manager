from django.conf import settings

class Manager_Config(object):
    @staticmethod
    def get_config():
        config = {
            'version': settings.VERSION,
            'paths': Manager_Config.get_paths(),
        }
        return config

    @staticmethod
    def get_paths():
        dictionary_paths = {
            ##################################################################
            # Project
            ##################################################################
            'url_api_projects': 'projects',
            'url_api_projects_check_uniqueness': 'info_projects/uniqueness',
            'url_api_ping': 'projects/{}/ping'.format(settings.PLACEHOLDER_SLUG_PROJECT),
            'url_api_projects_clear_sandbox': 'projects/{}/clear_sandbox'.format(settings.PLACEHOLDER_SLUG_PROJECT),
            'url_api_projects_tasks': 'projects/{}/tasks'.format(settings.PLACEHOLDER_SLUG_PROJECT),

            'url_api_projects_balance': 'projects/{}/balance'.format(settings.PLACEHOLDER_SLUG_PROJECT),
            'url_api_projects_finances': 'projects/{}/finances'.format(settings.PLACEHOLDER_SLUG_PROJECT),

            'url_api_projects_settings_batch': 'projects/{}/settings_batch'.format(settings.PLACEHOLDER_SLUG_PROJECT),
            'url_api_projects_settings_batch_all': 'projects/{}/settings_batch_all'.format(settings.PLACEHOLDER_SLUG_PROJECT),

            'url_api_projects_templates_worker': 'projects/{}/templates_worker'.format(settings.PLACEHOLDER_SLUG_PROJECT),
            'url_api_projects_templates_worker_all': 'projects/{}/templates_worker_all'.format(settings.PLACEHOLDER_SLUG_PROJECT),

            'url_api_projects_templates_assignment': 'projects/{}/templates_assignment'.format(settings.PLACEHOLDER_SLUG_PROJECT),
            'url_api_projects_templates_assignment_all': 'projects/{}/templates_assignment_all'.format(settings.PLACEHOLDER_SLUG_PROJECT),

            'url_api_projects_templates_hit': 'projects/{}/templates_hit'.format(settings.PLACEHOLDER_SLUG_PROJECT),
            'url_api_projects_templates_hit_all': 'projects/{}/templates_hit_all'.format(settings.PLACEHOLDER_SLUG_PROJECT),

            'url_api_projects_templates_global': 'projects/{}/templates_global'.format(settings.PLACEHOLDER_SLUG_PROJECT),
            'url_api_projects_templates_global_all': 'projects/{}/templates_global_all'.format(settings.PLACEHOLDER_SLUG_PROJECT),

            ##################################################################
            # Batches
            ##################################################################
            'url_api_batches': 'batches'.format(settings.PLACEHOLDER_SLUG_PROJECT),

            'url_api_projects_batches': 'projects/{}/batches'.format(settings.PLACEHOLDER_SLUG_PROJECT),
            'url_api_projects_batches_download': 'projects/{}/download_batches'.format(settings.PLACEHOLDER_SLUG_PROJECT),
            'url_api_projects_batches_download_info': 'projects/{}/download_info_batches'.format(settings.PLACEHOLDER_SLUG_PROJECT),

            ##################################################################
            # HITs
            ##################################################################
            'url_api_hits': 'hits'.format(settings.PLACEHOLDER_SLUG_PROJECT),

            'url_api_projects_hits': 'projects/{}/hits'.format(settings.PLACEHOLDER_SLUG_PROJECT),
            ##################################################################
            # Assignments
            ##################################################################
            'url_api_assignments': 'assignments'.format(settings.PLACEHOLDER_SLUG_PROJECT),

            'url_api_projects_assignments': 'projects/{}/assignments'.format(settings.PLACEHOLDER_SLUG_PROJECT),

            'url_api_workers': 'projects/{}/workers'.format(settings.PLACEHOLDER_SLUG_PROJECT),
            'url_api_workers_get_blocks_hard': 'projects/{}/workers/blocks_hard'.format(settings.PLACEHOLDER_SLUG_PROJECT),

            'url_api_keywords': 'keywords'.format(settings.PLACEHOLDER_SLUG_PROJECT),
            ##################################################################
            # Messages
            ##################################################################
            'url_api_messages_reject': 'messagesReject'.format(settings.PLACEHOLDER_SLUG_PROJECT),
            'url_api_messages_approve': 'messagesApprove'.format(settings.PLACEHOLDER_SLUG_PROJECT),
            'url_api_messages_reason': 'messagesReason'.format(settings.PLACEHOLDER_SLUG_PROJECT),

            'url_api_projects_messages_reject': 'projects/{}/messagesReject'.format(settings.PLACEHOLDER_SLUG_PROJECT),
            'url_api_projects_messages_approve': 'projects/{}/messagesApprove'.format(settings.PLACEHOLDER_SLUG_PROJECT),
            'url_api_projects_messages_reason': 'projects/{}/messagesReason'.format(settings.PLACEHOLDER_SLUG_PROJECT),
        }

        return dictionary_paths