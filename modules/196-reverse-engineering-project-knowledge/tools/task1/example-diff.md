# Example Diff: Implementation of Issue #47

```diff
diff --git a/src/models/notification-preference.model.ts b/src/models/notification-preference.model.ts
new file mode 100644
index 0000000..a3f8c12
--- /dev/null
+++ b/src/models/notification-preference.model.ts
@@ -0,0 +1,34 @@
+import { Entity, Column, PrimaryGeneratedColumn, ManyToOne, JoinColumn } from 'typeorm';
+import { User } from './user.model';
+
+export enum NotificationChannel {
+  EMAIL = 'email',
+  IN_APP = 'in_app',
+  SMS = 'sms',
+}
+
+export enum NotificationEventType {
+  ORDER_STATUS = 'order_status',
+  MARKETING = 'marketing',
+  SECURITY = 'security',
+}
+
+@Entity('notification_preferences')
+export class NotificationPreference {
+  @PrimaryGeneratedColumn('uuid')
+  id: string;
+
+  @ManyToOne(() => User, { onDelete: 'CASCADE' })
+  @JoinColumn({ name: 'user_id' })
+  user: User;
+
+  @Column({ type: 'enum', enum: NotificationChannel })
+  channel: NotificationChannel;
+
+  @Column({ type: 'enum', enum: NotificationEventType })
+  eventType: NotificationEventType;
+
+  @Column({ type: 'boolean', default: true })
+  enabled: boolean;
+}

diff --git a/src/services/notification-preference.service.ts b/src/services/notification-preference.service.ts
new file mode 100644
index 0000000..b7e2d91
--- /dev/null
+++ b/src/services/notification-preference.service.ts
@@ -0,0 +1,58 @@
+import { Injectable, BadRequestException } from '@nestjs/common';
+import { InjectRepository } from '@nestjs/typeorm';
+import { Repository } from 'typeorm';
+import { NotificationPreference, NotificationChannel, NotificationEventType } from '../models/notification-preference.model';
+
+@Injectable()
+export class NotificationPreferenceService {
+  constructor(
+    @InjectRepository(NotificationPreference)
+    private readonly prefRepo: Repository<NotificationPreference>,
+  ) {}
+
+  async getByUserId(userId: string): Promise<NotificationPreference[]> {
+    return this.prefRepo.find({
+      where: { user: { id: userId } },
+      order: { channel: 'ASC', eventType: 'ASC' },
+    });
+  }
+
+  async updatePreference(
+    userId: string,
+    channel: NotificationChannel,
+    eventType: NotificationEventType,
+    enabled: boolean,
+  ): Promise<NotificationPreference> {
+    if (eventType === NotificationEventType.SECURITY && !enabled) {
+      throw new BadRequestException('Security notifications cannot be disabled');
+    }
+
+    let pref = await this.prefRepo.findOne({
+      where: {
+        user: { id: userId },
+        channel,
+        eventType,
+      },
+    });
+
+    if (!pref) {
+      pref = this.prefRepo.create({
+        user: { id: userId },
+        channel,
+        eventType,
+        enabled,
+      });
+    } else {
+      pref.enabled = enabled;
+    }
+
+    return this.prefRepo.save(pref);
+  }
+
+  async initializeDefaults(userId: string): Promise<void> {
+    const channels = Object.values(NotificationChannel);
+    const events = Object.values(NotificationEventType);
+
+    const prefs = channels.flatMap(channel =>
+      events.map(eventType =>
+        this.prefRepo.create({ user: { id: userId }, channel, eventType, enabled: true }),
+      ),
+    );
+
+    await this.prefRepo.save(prefs);
+  }
+}

diff --git a/src/controllers/notification-preference.controller.ts b/src/controllers/notification-preference.controller.ts
new file mode 100644
index 0000000..c4d9e33
--- /dev/null
+++ b/src/controllers/notification-preference.controller.ts
@@ -0,0 +1,42 @@
+import { Controller, Get, Put, Param, Body, UseGuards } from '@nestjs/common';
+import { AuthGuard } from '../guards/auth.guard';
+import { OwnerGuard } from '../guards/owner.guard';
+import { NotificationPreferenceService } from '../services/notification-preference.service';
+import { UpdatePreferenceDto } from '../dto/update-preference.dto';
+
+@Controller('api/users/:userId/notification-preferences')
+@UseGuards(AuthGuard, OwnerGuard)
+export class NotificationPreferenceController {
+  constructor(
+    private readonly prefService: NotificationPreferenceService,
+  ) {}
+
+  @Get()
+  async getPreferences(@Param('userId') userId: string) {
+    return this.prefService.getByUserId(userId);
+  }
+
+  @Put()
+  async updatePreference(
+    @Param('userId') userId: string,
+    @Body() dto: UpdatePreferenceDto,
+  ) {
+    return this.prefService.updatePreference(
+      userId,
+      dto.channel,
+      dto.eventType,
+      dto.enabled,
+    );
+  }
+}

diff --git a/src/dto/update-preference.dto.ts b/src/dto/update-preference.dto.ts
new file mode 100644
index 0000000..e1a2b3c
--- /dev/null
+++ b/src/dto/update-preference.dto.ts
@@ -0,0 +1,18 @@
+import { IsEnum, IsBoolean } from 'class-validator';
+import { NotificationChannel, NotificationEventType } from '../models/notification-preference.model';
+
+export class UpdatePreferenceDto {
+  @IsEnum(NotificationChannel)
+  channel: NotificationChannel;
+
+  @IsEnum(NotificationEventType)
+  eventType: NotificationEventType;
+
+  @IsBoolean()
+  enabled: boolean;
+}

diff --git a/src/tests/notification-preference.service.spec.ts b/src/tests/notification-preference.service.spec.ts
new file mode 100644
index 0000000..f5c8a91
--- /dev/null
+++ b/src/tests/notification-preference.service.spec.ts
@@ -0,0 +1,47 @@
+import { Test } from '@nestjs/testing';
+import { getRepositoryToken } from '@nestjs/typeorm';
+import { BadRequestException } from '@nestjs/common';
+import { NotificationPreferenceService } from '../services/notification-preference.service';
+import { NotificationPreference, NotificationChannel, NotificationEventType } from '../models/notification-preference.model';
+
+describe('NotificationPreferenceService', () => {
+  let service: NotificationPreferenceService;
+  let mockRepo: any;
+
+  beforeEach(async () => {
+    mockRepo = {
+      find: jest.fn(),
+      findOne: jest.fn(),
+      create: jest.fn(dto => dto),
+      save: jest.fn(entity => Promise.resolve(entity)),
+    };
+
+    const module = await Test.createTestingModule({
+      providers: [
+        NotificationPreferenceService,
+        { provide: getRepositoryToken(NotificationPreference), useValue: mockRepo },
+      ],
+    }).compile();
+
+    service = module.get(NotificationPreferenceService);
+  });
+
+  it('should reject disabling security notifications', async () => {
+    await expect(
+      service.updatePreference('user-1', NotificationChannel.EMAIL, NotificationEventType.SECURITY, false),
+    ).rejects.toThrow(BadRequestException);
+  });
+
+  it('should create preference if not exists', async () => {
+    mockRepo.findOne.mockResolvedValue(null);
+    const result = await service.updatePreference(
+      'user-1', NotificationChannel.SMS, NotificationEventType.MARKETING, false,
+    );
+    expect(mockRepo.create).toHaveBeenCalled();
+    expect(result.enabled).toBe(false);
+  });
+
+  it('should initialize defaults for all channel-event combinations', async () => {
+    await service.initializeDefaults('user-1');
+    // 3 channels × 3 event types = 9 preferences
+    expect(mockRepo.save).toHaveBeenCalledWith(
+      expect.arrayContaining([expect.objectContaining({ enabled: true })]),
+    );
+  });
+});
```
