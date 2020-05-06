import gql from 'graphql-tag';

export const fragmentsTemplate = {
  templateWorker: gql`fragment templateWorker on TypeTemplateWorker {
    id
    name
    template
    isActive
    datetimeCreation
    heightFrame
    jsonDictParameters
    templateAssignment {
        id
    }
    templateGlobal {
        id
    }
    templateHit {
        id
    }
    templateOriginal {
        id
    } 
  }`,
  templateAssignment: gql`fragment templateAssignment on TypeTemplateAssignment {
    id
    name
    template
    isActive
    datetimeCreation
  }`,
  templateHIT: gql`fragment templateHIT on TypeTemplateHIT {
    id
    name
    template
    isActive
    datetimeCreation
  }`,
  templateGlobal: gql`fragment templateGlobal on TypeTemplateGlobal {
    id
    name
    template
    isActive
    datetimeCreation
  }`,
};
