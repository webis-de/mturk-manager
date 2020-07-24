import gql from 'graphql-tag';

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
