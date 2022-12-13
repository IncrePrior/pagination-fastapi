import { User } from './User';

export const Users = ({ users }) => {
  return (
    <div
      style={{
        overflow: 'scroll',
        maxHeight: '90vh',
        display: 'flex',
        flexFlow: 'row wrap',
        backgroundColor: '#b3dbff',
        height: '85vh',
      }}
    >
      {users.map((user, index) => (
        <User name={user.name} email={user.email} picture_url={user.picture} key={index} />
      ))}
    </div>
  );
};
