var keystone = require('keystone');
var Types = keystone.Field.Types;

/**
 * User Model
 * ==========
 */

var User = new keystone.List('User');

User.add({
	name: { type: Types.Name, required: true, initial: true, index: true },
	image: { type: Types.Url, index: true },
	email: { type: Types.Email, initial: true, required: true, index: true },
	g_token: { type: Types.Key, index: true, noedit: true },
	sail_level: { type: Types.Select, options: 'Beginner, Intermediate, Race', initial: true, required: true },
	year_level: { type: Types.Select, options: '1st, 2nd, 3rd, 4th, 5th', initial: true, required: true },
	eboard_pos: { type: Types.Text, required: false, index: true, dependsOn: { isEboard: [true] } },
	password: { type: Types.Password, initial: true, required: true }
}, 'Permissions', {
	isEboard: { type: Boolean, label: 'User is on the eboard', index: true },
	isAdmin: { type: Boolean, label: 'User is an admin', index: true }
});

// Provide access to Keystone
User.schema.virtual('canAccessKeystone').get(function() {
	return this.isEboard;
});


/**
 * Relationships
 */

User.relationship({ ref: 'Post', path: 'posts', refPath: 'author' });


/**
 * Registration
 */

User.defaultColumns = 'name, email, isEboard, isAdmin';
User.register();
