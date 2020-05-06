import gql from 'graphql-tag';

export const fragmentsTemplate = {
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
