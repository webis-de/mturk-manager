import gql from 'graphql-tag';
import { fragmentsTemplate } from '@/modules/template/template.fragment';

export const queryTemplates = gql`query templates($project: ID!){
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
