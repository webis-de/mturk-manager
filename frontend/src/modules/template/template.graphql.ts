import gql from 'graphql-tag';
import { fragmentsTemplate } from '@/modules/template/template.fragment';

export const queryTemplates = gql`query templates($project: ID!){
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
${fragmentsTemplate.templateAssignment}
${fragmentsTemplate.templateHIT}
${fragmentsTemplate.templateGlobal}
`;
