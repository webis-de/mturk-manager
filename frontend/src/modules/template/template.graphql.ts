import gql from 'graphql-tag';
import { fragmentsTemplate } from '@/modules/template/template.fragment';

export const queryTemplates = gql`{
    templatesAssignment {
        ...templateAssignment
    }
    templatesHit {
        ...templateHIT
    }
    templatesGlobal {
        ...templateGlobal
    }
}
${fragmentsTemplate.templateAssignment}
${fragmentsTemplate.templateHIT}
${fragmentsTemplate.templateGlobal}
`;
