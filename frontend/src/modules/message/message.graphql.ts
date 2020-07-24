import gql from 'graphql-tag';

export const queryMessagesReject = gql`query messagesReject($project: ID!) {
    messagesReject(project: $project) {
        id
        message
    }
}`;
export const queryMessagesRejectSearch = gql`query searchMessagesReject($message: String!) {
    searchMessagesReject(message: $message, limit: 7) {
        id
        message
    }
}`;
/**
 * Create
 */
export const mutationCreateMessageReject = gql`mutation createMessageReject($message: InputMessageReject!) {
    createMessageReject(message: $message) {
        message {
            id
            message
        }
    }
}
`;
/**
 * Delete
 */
export const mutationDeleteMessageReject = gql`mutation deleteMessageReject($id: ID!) {
    deleteMessageReject(idMessage: $id) {
        idMessage
    }
}
`;
