"""
Example demonstrating list operations for roles, permissions, and permission groups.
"""

import asyncio

from rbac import RBAC


async def main():
	# Initialize RBAC
	rbac = RBAC(
		database_url="postgresql+asyncpg://hexa:hexa@localhost/hexa",
		adapter="sqlalchemy",
	)

	await rbac.init()

	try:
		print("=" * 80)
		print("RBAC List Operations Example")
		print("=" * 80)

		# List all permissions
		print("\n1. Listing all permissions:")
		print("-" * 80)
		permissions_result = await rbac.service.get_list_of_permissions()
		if permissions_result.success:
			print(f"✅ Found {len(permissions_result.data)} permissions:")
			for perm in permissions_result.data:
				print(f"   - {perm.name} ({perm.category}): {perm.display_name}")
		else:
			print(f"❌ Error: {permissions_result.error}")

		# List all permission groups
		print("\n2. Listing all permission groups:")
		print("-" * 80)
		groups_result = await rbac.service.get_list_of_permission_groups()
		if groups_result.success:
			print(f"✅ Found {len(groups_result.data)} permission groups:")
			for group in groups_result.data:
				print(
					f"   - {group.name}: {group.display_name} "
					f"({group.permission_count} permissions)"
				)
		else:
			print(f"❌ Error: {groups_result.error}")

		# List all roles
		print("\n3. Listing all roles:")
		print("-" * 80)
		roles_result = await rbac.service.get_list_of_roles()
		if roles_result.success:
			print(f"✅ Found {len(roles_result.data)} roles:")
			for role in roles_result.data:
				print(f"   - {role.name}: {role.display_name}")
				if role.description:
					print(f"     Description: {role.description}")
		else:
			print(f"❌ Error: {roles_result.error}")

		# Summary
		print("\n" + "=" * 80)
		print("SUMMARY")
		print("=" * 80)
		if permissions_result.success:
			print(f"Total Permissions: {len(permissions_result.data)}")
		if groups_result.success:
			print(f"Total Permission Groups: {len(groups_result.data)}")
		if roles_result.success:
			print(f"Total Roles: {len(roles_result.data)}")
		print("=" * 80)

	finally:
		await rbac.close()


if __name__ == "__main__":
	asyncio.run(main())
