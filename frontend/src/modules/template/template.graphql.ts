import gql from 'graphql-tag';
import { fragmentsTemplate } from '@/modules/template/template.fragment';

export const queryTemplates = gql`query templates($project: ID!) {
    templatesWorker(project: $project) {
        ...templateWorker
    }
    templatesAssignment(project: $project) {
        ...templateAssignment
    }
    templatesHit(project: $project) {
        ...templateHIT
    }
    templatesGlobal(project: $project) {
        ...templateGlobal
    }
}
${fragmentsTemplate.templateWorker}
${fragmentsTemplate.templateAssignment}
${fragmentsTemplate.templateHIT}
${fragmentsTemplate.templateGlobal}
`;
/**
 * Create
 */
export const queryCreateTemplateWorker = gql`mutation createTemplateWorker($template: InputTemplateWorker!) {
    createTemplateWorker(template: $template) {
        template {
            ...templateWorker
        }
    }
}
${fragmentsTemplate.templateWorker}
`;
export const queryCreateTemplateAssignment = gql`mutation createTemplateAssignment($template: InputTemplateAssignment!) {
    createTemplateAssignment(template: $template) {
        template {
            ...templateAssignment
        }
    }
}
${fragmentsTemplate.templateAssignment}
`;
export const queryCreateTemplateHIT = gql`mutation createTemplateHIT($template: InputTemplateHIT!) {
    createTemplateHit(template: $template) {
        template {
            ...templateHIT
        }
    }
}
${fragmentsTemplate.templateHIT}
`;
export const queryCreateTemplateGlobal = gql`mutation createTemplateGlobal ($template: InputTemplateGlobal !) {
    createTemplateGlobal (template: $template) {
        template {
            ...templateGlobal 
        }
    }
}
${fragmentsTemplate.templateGlobal }
`;
/**
 * Update
 */
export const queryUpdateTemplateWorker = gql`mutation updateTemplateWorker($template: InputTemplateWorker!) {
    updateTemplateWorker(template: $template) {
        template {
            ...templateWorker
        }
    }
}
${fragmentsTemplate.templateWorker}
`;
export const queryUpdateTemplateAssignment = gql`mutation updateTemplateAssignment($template: InputTemplateAssignment!) {
    updateTemplateAssignment(template: $template) {
        template {
            ...templateAssignment
        }
    }
}
${fragmentsTemplate.templateAssignment}
`;
export const queryUpdateTemplateHIT = gql`mutation updateTemplateHIT($template: InputTemplateHIT!) {
    updateTemplateHit(template: $template) {
        template {
            ...templateHIT
        }
    }
}
${fragmentsTemplate.templateHIT}
`;
export const queryUpdateTemplateGlobal = gql`mutation updateTemplateGlobal($template: InputTemplateGlobal!) {
    updateTemplateGlobal(template: $template) {
        template {
            ...templateGlobal
        }
    }
}
${fragmentsTemplate.templateGlobal}
`;
/**
 * Delete
 */
export const queryDeleteTemplateWorker = gql`mutation deleteTemplateWorker($id: ID!) {
    deleteTemplateWorker(idTemplate: $id) {
        idTemplate
    }
}`;
export const queryDeleteTemplateAssignment = gql`mutation deleteTemplateAssignment($id: ID!) {
    deleteTemplateAssignment(idTemplate: $id) {
        idTemplate
    }
}`;
export const queryDeleteTemplateHIT = gql`mutation deleteTemplateHIT($id: ID!) {
    deleteTemplateHit(idTemplate: $id) {
        idTemplate
    }
}`;
export const queryDeleteTemplateGlobal = gql`mutation deleteTemplateGlobal($id: ID!) {
    deleteTemplateGlobal(idTemplate: $id) {
        idTemplate
    }
}`;
